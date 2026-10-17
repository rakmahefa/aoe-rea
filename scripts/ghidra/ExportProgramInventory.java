// Export a reproducible, read-only inventory from a Ghidra-imported program.
// Run with:
//   analyzeHeadless <project-dir> <project-name> -import <binary> \
//     -scriptPath scripts/ghidra -postScript ExportProgramInventory.java <out-dir> <sha256> <commit> <target-path> <ghidra-version>
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressRange;
import ghidra.program.model.address.AddressRangeIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.ExternalManager;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class ExportProgramInventory extends GhidraScript {

    private String address(Address value) {
        if (value == null) {
            return "";
        }
        return "0x" + value.toString().toLowerCase(Locale.ROOT);
    }

    private String csv(String value) {
        if (value == null) {
            return "";
        }
        if (value.contains(",") || value.contains("\"") || value.contains("\n") || value.contains("\r")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }

    private String json(String value) {
        if (value == null) {
            return "null";
        }
        StringBuilder out = new StringBuilder("\"");
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            switch (c) {
                case '"': out.append("\\\""); break;
                case '\\': out.append("\\\\"); break;
                case '\n': out.append("\\n"); break;
                case '\r': out.append("\\r"); break;
                case '\t': out.append("\\t"); break;
                default:
                    if (c < 0x20) {
                        out.append(String.format("\\u%04x", (int)c));
                    } else {
                        out.append(c);
                    }
            }
        }
        out.append('"');
        return out.toString();
    }

    private void writeLine(BufferedWriter writer, String line) throws Exception {
        writer.write(line);
        writer.newLine();
    }

    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 5) {
            throw new IllegalArgumentException(
                "Expected arguments: <output-dir> <target-sha256> <source-commit> <target-path> <ghidra-version>");
        }

        File outDir = new File(args[0]);
        if (!outDir.exists() && !outDir.mkdirs()) {
            throw new IllegalStateException("Cannot create output directory: " + outDir);
        }
        if (!outDir.isDirectory()) {
            throw new IllegalArgumentException("Output path is not a directory: " + outDir);
        }

        File functionsFile = new File(outDir, "functions.csv");
        File rangesFile = new File(outDir, "function_ranges.csv");
        File blocksFile = new File(outDir, "memory_blocks.csv");
        File librariesFile = new File(outDir, "external_libraries.csv");
        File summaryFile = new File(outDir, "summary.json");

        long totalFunctions = 0;
        long internalFunctions = 0;
        long externalFunctions = 0;
        long thunkFunctions = 0;
        long totalFunctionBodyBytes = 0;
        long totalFunctionBodyRanges = 0;

        FunctionManager manager = currentProgram.getFunctionManager();
        monitor.setMessage("Exporting Ghidra function inventory");

        try (BufferedWriter functions = new BufferedWriter(
                 new OutputStreamWriter(new FileOutputStream(functionsFile), StandardCharsets.UTF_8));
             BufferedWriter ranges = new BufferedWriter(
                 new OutputStreamWriter(new FileOutputStream(rangesFile), StandardCharsets.UTF_8))) {

            writeLine(functions, "entry_address,name,is_external,is_thunk,body_bytes,body_range_count");
            writeLine(ranges, "function_entry,name,range_index,start_address,end_address,range_bytes");

            FunctionIterator iterator = manager.getFunctions(true);
            while (iterator.hasNext()) {
                monitor.checkCancelled();
                Function function = iterator.next();
                totalFunctions++;

                boolean external = function.isExternal();
                boolean thunk = function.isThunk();
                if (external) {
                    externalFunctions++;
                } else {
                    internalFunctions++;
                }
                if (thunk) {
                    thunkFunctions++;
                }

                long bodyBytes = 0;
                long rangeCount = 0;
                AddressRangeIterator bodyRanges = function.getBody().getAddressRanges();
                while (bodyRanges.hasNext()) {
                    AddressRange range = bodyRanges.next();
                    rangeCount++;
                    long length = range.getLength();
                    bodyBytes += length;
                    totalFunctionBodyBytes += length;
                    totalFunctionBodyRanges++;
                    writeLine(ranges,
                        csv(address(function.getEntryPoint())) + "," +
                        csv(function.getName()) + "," +
                        rangeCount + "," +
                        csv(address(range.getMinAddress())) + "," +
                        csv(address(range.getMaxAddress())) + "," +
                        length);
                }

                writeLine(functions,
                    csv(address(function.getEntryPoint())) + "," +
                    csv(function.getName()) + "," +
                    external + "," +
                    thunk + "," +
                    bodyBytes + "," +
                    rangeCount);
            }
        }

        long memoryBlockCount = 0;
        long memoryBlockBytes = 0;
        monitor.setMessage("Exporting memory-block inventory");
        try (BufferedWriter blocks = new BufferedWriter(
                 new OutputStreamWriter(new FileOutputStream(blocksFile), StandardCharsets.UTF_8))) {
            writeLine(blocks, "name,start_address,end_address,size_bytes,read,write,execute,initialized");
            for (MemoryBlock block : currentProgram.getMemory().getBlocks()) {
                monitor.checkCancelled();
                memoryBlockCount++;
                memoryBlockBytes += block.getSize();
                writeLine(blocks,
                    csv(block.getName()) + "," +
                    csv(address(block.getStart())) + "," +
                    csv(address(block.getEnd())) + "," +
                    block.getSize() + "," +
                    block.isRead() + "," +
                    block.isWrite() + "," +
                    block.isExecute() + "," +
                    block.isInitialized());
            }
        }

        ExternalManager externalManager = currentProgram.getExternalManager();
        String[] libraries = externalManager.getExternalLibraryNames();
        if (libraries == null) {
            libraries = new String[0];
        }
        try (BufferedWriter libraryWriter = new BufferedWriter(
                 new OutputStreamWriter(new FileOutputStream(librariesFile), StandardCharsets.UTF_8))) {
            writeLine(libraryWriter, "library_name");
            for (String library : libraries) {
                writeLine(libraryWriter, csv(library));
            }
        }

        StringBuilder summary = new StringBuilder();
        summary.append("{\n");
        summary.append("  \"schema_version\": 1,\n");
        summary.append("  \"target\": {\n");
        summary.append("    \"path\": ").append(json(args[3])).append(",\n");
        summary.append("    \"sha256\": ").append(json(args[1])).append(",\n");
        summary.append("    \"source_commit\": ").append(json(args[2])).append("\n");
        summary.append("  },\n");
        summary.append("  \"analysis\": {\n");
        summary.append("    \"provider\": \"Ghidra headless\",\n");
        summary.append("    \"ghidra_version\": ").append(json(args[4])).append(",\n");
        summary.append("    \"program_name\": ").append(json(currentProgram.getName())).append(",\n");
        summary.append("    \"executable_format\": ").append(json(currentProgram.getExecutableFormat())).append(",\n");
        summary.append("    \"language_id\": ").append(json(currentProgram.getLanguageID().getIdAsString())).append(",\n");
        summary.append("    \"compiler_spec_id\": ").append(json(currentProgram.getCompilerSpec().getCompilerSpecID().getIdAsString())).append(",\n");
        summary.append("    \"image_base\": ").append(json(address(currentProgram.getImageBase()))).append("\n");
        summary.append("  },\n");
        summary.append("  \"functions\": {\n");
        summary.append("    \"total\": ").append(totalFunctions).append(",\n");
        summary.append("    \"internal\": ").append(internalFunctions).append(",\n");
        summary.append("    \"external\": ").append(externalFunctions).append(",\n");
        summary.append("    \"thunks\": ").append(thunkFunctions).append(",\n");
        summary.append("    \"body_bytes_sum\": ").append(totalFunctionBodyBytes).append(",\n");
        summary.append("    \"body_ranges_sum\": ").append(totalFunctionBodyRanges).append("\n");
        summary.append("  },\n");
        summary.append("  \"memory\": {\n");
        summary.append("    \"block_count\": ").append(memoryBlockCount).append(",\n");
        summary.append("    \"block_bytes_sum\": ").append(memoryBlockBytes).append("\n");
        summary.append("  },\n");
        summary.append("  \"external_library_count\": ").append(libraries.length).append(",\n");
        summary.append("  \"files\": {\n");
        summary.append("    \"functions\": \"functions.csv\",\n");
        summary.append("    \"function_ranges\": \"function_ranges.csv\",\n");
        summary.append("    \"memory_blocks\": \"memory_blocks.csv\",\n");
        summary.append("    \"external_libraries\": \"external_libraries.csv\"\n");
        summary.append("  }\n");
        summary.append("}\n");

        try (BufferedWriter writer = new BufferedWriter(
                 new OutputStreamWriter(new FileOutputStream(summaryFile), StandardCharsets.UTF_8))) {
            writer.write(summary.toString());
        }

        println("Program inventory exported to " + outDir.getAbsolutePath());
        println("Functions total=" + totalFunctions +
            ", internal=" + internalFunctions +
            ", external=" + externalFunctions +
            ", thunks=" + thunkFunctions);
        println("Memory blocks=" + memoryBlockCount +
            ", external libraries=" + libraries.length);
    }
}
