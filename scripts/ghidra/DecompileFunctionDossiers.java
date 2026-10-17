// Decompile every Ghidra function in bounded batches of 100 using Ghidra's parallel decompiler.
// Args: <output-root> <target-sha256> <source-commit> <target-path> <ghidra-version>
import generic.cache.CachingPool;
import generic.cache.CountingBasicFactory;
import generic.concurrent.QCallback;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.decompiler.parallel.ChunkingParallelDecompiler;
import ghidra.app.decompiler.parallel.ParallelDecompiler;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Program;
import ghidra.util.exception.CancelledException;
import ghidra.util.task.CancelledListener;
import ghidra.util.task.TaskMonitor;
import ghidra.util.task.TaskMonitorAdapter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class DecompileFunctionDossiers extends GhidraScript {
    private static final int BATCH_SIZE = 100;
    private File outputRoot;
    private String targetSha;
    private String sourceCommit;
    private String targetPath;
    private String ghidraVersion;
    private Map<String, Long> indexByAddress;

    private String clean(String s) {
        if (s == null || s.isEmpty()) return "unnamed";
        return s.replaceAll("[^A-Za-z0-9._-]+", "_");
    }

    private String addr(Address a) {
        return a == null ? "unknown" : "0x" + a.toString().toLowerCase(Locale.ROOT);
    }

    private void write(BufferedWriter w, String s) throws IOException {
        w.write(s);
        w.newLine();
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 5) {
            throw new IllegalArgumentException(
                "Expected output-root, target-sha256, source-commit, target-path, ghidra-version");
        }

        outputRoot = new File(args[0]);
        targetSha = args[1];
        sourceCommit = args[2];
        targetPath = args[3];
        ghidraVersion = args[4];

        File functionsRoot = new File(outputRoot, "functions");
        if (!functionsRoot.exists() && !functionsRoot.mkdirs()) {
            throw new IllegalStateException("Cannot create " + functionsRoot);
        }

        List<Function> functions = new ArrayList<>();
        indexByAddress = new HashMap<>();
        FunctionIterator iterator = currentProgram.getFunctionManager().getFunctions(true);
        long nextIndex = 0;
        while (iterator.hasNext()) {
            monitor.checkCancelled();
            Function function = iterator.next();
            functions.add(function);
            indexByAddress.put(addr(function.getEntryPoint()), nextIndex++);
        }

        long total = functions.size();
        if (total == 0) {
            throw new IllegalStateException("Ghidra returned no function entries; refusing to publish an empty report.");
        }

        ChunkingTaskMonitor chunkMonitor = new ChunkingTaskMonitor(monitor);
        chunkMonitor.doInitialize(total);
        CachingPool<DecompInterface> decompilerPool =
            new CachingPool<>(new DecompilerFactory(currentProgram));
        FunctionDossierCallback callback = new FunctionDossierCallback(decompilerPool, chunkMonitor);
        ChunkingParallelDecompiler<FunctionDossier> parallelDecompiler =
            ParallelDecompiler.createChunkingParallelDecompiler(callback, chunkMonitor);

        long completed = 0;
        long succeeded = 0;
        long failed = 0;
        long external = 0;
        long batchNumber = 0;
        File indexFile = new File(outputRoot, "index.csv");

        try (BufferedWriter indexWriter = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(indexFile), StandardCharsets.UTF_8))) {
            write(indexWriter, "index,address,name,thunk,external,decompile_status,note_file");
            indexWriter.flush();

            for (int start = 0; start < functions.size(); start += BATCH_SIZE) {
                monitor.checkCancelled();
                int end = Math.min(start + BATCH_SIZE, functions.size());
                List<Function> batch = new ArrayList<>(functions.subList(start, end));
                chunkMonitor.setBatchOffset(start);

                List<FunctionDossier> rows = parallelDecompiler.decompileFunctions(batch);
                if (rows == null || rows.size() != batch.size()) {
                    throw new IllegalStateException(
                        "Batch " + (batchNumber + 1) + " returned " +
                        (rows == null ? "null" : rows.size()) + " results for " + batch.size() + " functions.");
                }
                Collections.sort(rows, Comparator.comparingLong(row -> row.index));

                for (FunctionDossier row : rows) {
                    String csvName = "\"" + row.name.replace("\"", "\"\"") + "\"";
                    write(indexWriter, row.index + "," + row.address + "," + csvName + "," +
                        row.thunk + "," + row.external + "," + row.status + "," + row.notePath);
                    if ("ok".equals(row.status)) succeeded++;
                    else if ("failed".equals(row.status)) failed++;
                    else if ("external".equals(row.status)) external++;
                }

                completed += rows.size();
                batchNumber++;
                indexWriter.flush(); // checkpoint the index after each completed batch of 100
                monitor.setProgress(completed);
                monitor.setMessage("Function dossiers: " + completed + " / " + total);
                println("Batch " + batchNumber + " complete: functions " + start + "–" + (end - 1) +
                    " (" + completed + "/" + total + "); decompiled=" + succeeded +
                    "; failed=" + failed + "; external=" + external);
            }
        }
        finally {
            parallelDecompiler.dispose();
            decompilerPool.dispose();
        }

        try (BufferedWriter w = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(new File(outputRoot, "README.md")), StandardCharsets.UTF_8))) {
            write(w, "# Automatic function dossiers");
            write(w, "");
            write(w, "- Target SHA-256: " + targetSha);
            write(w, "- Source commit: " + sourceCommit);
            write(w, "- Ghidra: " + ghidraVersion);
            write(w, "- Functions indexed: " + completed + " / " + total);
            write(w, "- Batch size: " + BATCH_SIZE);
            write(w, "- Completed batches: " + batchNumber);
            write(w, "- Parallel decompilation: Ghidra ParallelDecompiler with its managed decompiler pool");
            write(w, "- Decompilation succeeded: " + succeeded);
            write(w, "- Decompilation failed: " + failed);
            write(w, "- External entries: " + external);
            write(w, "");
            write(w, "Every 100-function batch is written to index.csv and flushed before the next batch. " +
                "Each indexed entry has a corresponding Markdown note under functions/<address-prefix>/. " +
                "A successful decompilation is static-analysis output, not semantic or runtime validation.");
        }
        println("Finished function dossiers: total=" + completed + "/" + total +
            ", batches=" + batchNumber + ", succeeded=" + succeeded +
            ", failed=" + failed + ", external=" + external);
    }

    private FunctionDossier writeDossier(Function function, long index, String status, String code)
            throws IOException {
        String address = addr(function.getEntryPoint());
        String name = function.getName();
        String prefix = address.length() >= 4 ? address.substring(2, 4) : "xx";
        File dir = new File(new File(outputRoot, "functions"), prefix);
        if (!dir.exists() && !dir.mkdirs()) throw new IOException("Cannot create " + dir);

        String filename = address + "_" + clean(name) + ".md";
        File note = new File(dir, filename);
        try (BufferedWriter w = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(note), StandardCharsets.UTF_8))) {
            write(w, "# Function dossier: " + name);
            write(w, "");
            write(w, "- Global function index: " + index);
            write(w, "- Entry: " + address);
            write(w, "- Ghidra name: " + name);
            write(w, "- Thunk: " + function.isThunk());
            write(w, "- External: " + function.isExternal());
            write(w, "- Decompilation status: **" + status + "**");
            write(w, "- Target SHA-256: " + targetSha);
            write(w, "- Source commit: " + sourceCommit);
            write(w, "- Target path: " + targetPath);
            write(w, "- Ghidra version: " + ghidraVersion);
            write(w, "");
            write(w, "> Automatically generated static-analysis note. Pseudocode is a hypothesis produced by the decompiler, not validated source or proof of runtime behavior. Record arguments, side effects, callers/callees, unknowns and differential tests in a reviewed dossier before marking the function understood.");
            write(w, "");
            write(w, "## Decompiler output");
            write(w, "");
            for (String line : code.split("\\R", -1)) write(w, "    " + line);
        }

        String relativePath = "functions/" + prefix + "/" + filename;
        return new FunctionDossier(index, address, name, function.isThunk(),
            function.isExternal(), status, relativePath);
    }

    private class FunctionDossierCallback implements QCallback<Function, FunctionDossier> {
        private final CachingPool<DecompInterface> pool;
        private final ChunkingTaskMonitor chunkMonitor;

        FunctionDossierCallback(CachingPool<DecompInterface> pool, ChunkingTaskMonitor chunkMonitor) {
            this.pool = pool;
            this.chunkMonitor = chunkMonitor;
        }

        @Override
        public FunctionDossier process(Function function, TaskMonitor taskMonitor) throws Exception {
            String address = addr(function.getEntryPoint());
            Long index = indexByAddress.get(address);
            if (index == null) throw new IllegalStateException("No index assigned to function " + address);

            if (function.isExternal()) {
                return writeDossier(function, index, "external", "");
            }

            DecompInterface decompiler = pool.get();
            try {
                DecompileResults result = decompiler.decompileFunction(function, 30, taskMonitor);
                String status;
                String code;
                if (result != null && result.decompileCompleted() &&
                        result.getDecompiledFunction() != null) {
                    status = "ok";
                    code = result.getDecompiledFunction().getC();
                }
                else {
                    status = "failed";
                    code = "/* Decompilation unavailable: " +
                        (result == null ? "no result" : result.getErrorMessage()) + " */";
                }
                return writeDossier(function, index, status, code);
            }
            finally {
                pool.release(decompiler);
            }
        }

        @Override
        public synchronized void addCancelledListener(CancelledListener listener) {
            chunkMonitor.addCancelledListener(listener);
        }

        @Override
        public synchronized void removeCancelledListener(CancelledListener listener) {
            chunkMonitor.removeCancelledListener(listener);
        }
    }

    private class DecompilerFactory extends CountingBasicFactory<DecompInterface> {
        private final Program program;

        DecompilerFactory(Program program) {
            this.program = program;
        }

        @Override
        public DecompInterface doCreate(int itemNumber) throws IOException {
            DecompInterface decompiler = new DecompInterface();
            decompiler.toggleCCode(true);
            decompiler.toggleSyntaxTree(false);
            if (!decompiler.openProgram(program)) {
                decompiler.dispose();
                throw new IOException("Decompiler failed to open program (pool item " + itemNumber + ")");
            }
            return decompiler;
        }

        @Override
        public void doDispose(DecompInterface decompiler) {
            decompiler.dispose();
        }
    }

    private class FunctionDossier {
        final long index;
        final String address;
        final String name;
        final boolean thunk;
        final boolean external;
        final String status;
        final String notePath;

        FunctionDossier(long index, String address, String name, boolean thunk,
                boolean external, String status, String notePath) {
            this.index = index;
            this.address = address;
            this.name = name;
            this.thunk = thunk;
            this.external = external;
            this.status = status;
            this.notePath = notePath;
        }
    }

    private class ChunkingTaskMonitor extends TaskMonitorAdapter {
        private final TaskMonitor delegate;
        private long batchOffset;
        private long total;

        ChunkingTaskMonitor(TaskMonitor delegate) {
            this.delegate = delegate;
        }

        void doInitialize(long value) {
            total = value;
            delegate.initialize(value);
        }

        void setBatchOffset(long value) {
            batchOffset = value;
        }

        @Override
        public void setProgress(long value) {
            delegate.setProgress(Math.min(total, batchOffset + value));
        }

        @Override
        public void checkCanceled() throws CancelledException {
            delegate.checkCanceled();
        }

        @Override
        public void setMessage(String message) {
            delegate.setMessage(message);
        }

        @Override
        public synchronized void addCancelledListener(CancelledListener listener) {
            delegate.addCancelledListener(listener);
        }

        @Override
        public synchronized void removeCancelledListener(CancelledListener listener) {
            delegate.removeCancelledListener(listener);
        }
    }
}
