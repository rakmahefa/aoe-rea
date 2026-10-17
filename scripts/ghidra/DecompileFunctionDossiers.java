// Decompile every Ghidra function and write one Markdown dossier per function.
// Args: <output-root> <target-sha256> <source-commit> <target-path> <ghidra-version>
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class DecompileFunctionDossiers extends GhidraScript {
    private String clean(String s) {
        if (s == null || s.isEmpty()) return "unnamed";
        return s.replaceAll("[^A-Za-z0-9._-]+", "_");
    }
    private String addr(Address a) {
        return a == null ? "unknown" : "0x" + a.toString().toLowerCase(Locale.ROOT);
    }
    private void write(BufferedWriter w, String s) throws Exception {
        w.write(s);
        w.newLine();
    }
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 5) throw new IllegalArgumentException("Expected output-root, target-sha256, source-commit, target-path, ghidra-version");
        File root = new File(args[0], "functions");
        if (!root.exists() && !root.mkdirs()) throw new IllegalStateException("Cannot create " + root);
        DecompInterface decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(false);
        if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException("Decompiler failed to open program");
        long index = 0, succeeded = 0, failed = 0;
        File indexFile = new File(args[0], "index.csv");
        try (BufferedWriter indexWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(indexFile), StandardCharsets.UTF_8))) {
            write(indexWriter, "index,address,name,thunk,external,decompile_status,note_file");
            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            while (it.hasNext()) {
                monitor.checkCancelled();
                Function f = it.next();
                String address = addr(f.getEntryPoint());
                String name = f.getName();
                String prefix = address.length() >= 4 ? address.substring(2, 4) : "xx";
                File dir = new File(root, prefix);
                if (!dir.exists() && !dir.mkdirs()) throw new IllegalStateException("Cannot create " + dir);
                String filename = address + "_" + clean(name) + ".md";
                File note = new File(dir, filename);
                DecompileResults result = null;
                String status = "external";
                String code = "";
                if (!f.isExternal()) {
                    result = decompiler.decompileFunction(f, 30, monitor);
                    if (result != null && result.decompileCompleted() && result.getDecompiledFunction() != null) {
                        status = "ok";
                        code = result.getDecompiledFunction().getC();
                        succeeded++;
                    } else {
                        status = "failed";
                        failed++;
                        code = "/* Decompilation unavailable: " + (result == null ? "no result" : result.getErrorMessage()) + " */";
                    }
                }
                try (BufferedWriter w = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(note), StandardCharsets.UTF_8))) {
                    write(w, "# Function dossier: " + name);
                    write(w, "");
                    write(w, "- Entry: `" + address + "`");
                    write(w, "- Ghidra name: `" + name + "`");
                    write(w, "- Thunk: " + f.isThunk());
                    write(w, "- External: " + f.isExternal());
                    write(w, "- Decompilation status: **" + status + "**");
                    write(w, "- Target SHA-256: `" + args[1] + "`");
                    write(w, "- Source commit: `" + args[2] + "`");
                    write(w, "- Target path: `" + args[3] + "`");
                    write(w, "- Ghidra version: " + args[4]);
                    write(w, "");
                    write(w, "> Automatically generated static-analysis note. Pseudocode is a hypothesis produced by the decompiler, not validated source or proof of runtime behavior. Record arguments, side effects, callers/callees, unknowns and differential tests in a reviewed dossier before marking the function understood.");
                    write(w, "");
                    write(w, "## Decompiler output");
                    write(w, "");
                    write(w, "```c");
                    for (String line : code.split("\\R", -1)) write(w, line);
                    write(w, "```");
                }
                String csvName = "\"" + name.replace("\"", "\"\"") + "\"";
                String notePath = "functions/" + prefix + "/" + filename;
                write(indexWriter, index + "," + address + "," + csvName + "," + f.isThunk() + "," + f.isExternal() + "," + status + "," + notePath);
                index++;
                if (index % 100 == 0) {
                    monitor.setMessage("Function dossiers: " + index + " / " + currentProgram.getFunctionManager().getFunctionCount());
                    println("Dossier progress: " + index + " functions; decompiled=" + succeeded + "; failed=" + failed);
                }
            }
        } finally {
            decompiler.dispose();
        }
        try (BufferedWriter w = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(args[0], "README.md")), StandardCharsets.UTF_8))) {
            write(w, "# Automatic function dossiers");
            write(w, "");
            write(w, "- Target SHA-256: `" + args[1] + "`");
            write(w, "- Source commit: `" + args[2] + "`");
            write(w, "- Ghidra: " + args[4]);
            write(w, "- Functions indexed: " + index);
            write(w, "- Decompilation succeeded: " + succeeded);
            write(w, "- Decompilation failed: " + failed);
            write(w, "");
            write(w, "Every entry in `index.csv` has a corresponding Markdown note under `functions/<address-prefix>/`. A successful decompilation is not semantic validation.");
        }
        println("Finished function dossiers: total=" + index + ", succeeded=" + succeeded + ", failed=" + failed);
    }
}
