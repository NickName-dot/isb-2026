import java.io.*;

public class Generator {
    private long state0, state1;
    
    public Generator(long seed) {
        state0 = seed;
        state1 = 1234567890123456789L;
        nextLong();
    }
    
    private long nextLong() {
        long s1 = state0;
        long s0 = state1;
        state0 = s0;
        s1 ^= s1 << 23;
        state1 = s1 ^ s0 ^ (s1 >>> 17) ^ (s0 >>> 26);
        return state1;
    }
    
    public int nextBit() {
        return (int)((nextLong() >>> 63) & 1);
    }
    
    public static void main(String[] args) {
        int count = 1000;
        PrintWriter out = new PrintWriter(System.out);
        String filename = null;
        
        try {
            if (args.length > 0) {
                count = Integer.parseInt(args[0]);
                if (count <= 0) count = 1000;
            }
            if (args.length > 1) {
                filename = args[1];
                out = new PrintWriter(new FileWriter(filename));
            }
            
            Generator rng = new Generator(12345);
            
            for (int i = 0; i < count; i++) {
                out.print(rng.nextBit());
            }
            
            out.flush();
            if (filename != null) {
                out.close();
                System.out.println(count + " БИТОВ записано в " + filename);
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
