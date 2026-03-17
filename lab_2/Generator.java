
public class Generator {
    private long seed = 0;
    private static final long A = 6364136223846793005L;
    private static final long C = 1442695040888963407L;
    
    public Generator(long seed) {
        this.seed = seed;
    }
    
    public int nextBit() {
        seed = seed * A + C;
        return (int)(seed & 1);
    }
    
    public static void main(String[] args) {
        int count = 128;
        java.io.PrintStream output = System.out;
        
        if (args.length > 0) {
            try {
                count = Integer.parseInt(args[0]);
                if (count <= 0) count = 128;
            } catch (NumberFormatException e) {
                count = 128;
            }
        }
        
        if (args.length > 1) {
            try {
                output = new java.io.PrintStream(new java.io.FileOutputStream(args[1]));
            } catch (java.io.FileNotFoundException e) {
                System.err.println("Ошибка файла");
                System.exit(1);
            }
        }
        
        Generator generator = new Generator(12345);
        
        for (int i = 0; i < count; i++) {
            output.print(generator.nextBit());
        }
        
        if (args.length > 1) {
            output.close();
            System.out.println(count + " БИТОВ записано");
        }
    }
}
