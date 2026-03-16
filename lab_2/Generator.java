import java.io.*;
import java.time.Instant;

class LCG {
    private long seed = 0;
    private static final long A = 6364136223846793005L;
    private static final long C = 1442695040888963407L;
    
    public LCG(long seed) {
        this.seed = seed;
    }
    
    public void setSeed(long s) {
        this.seed = s;
    }
    
    public long next() {
        seed = (seed * A + C) % (1L << 64);
        return seed;
    }
    
    public int nextInt(int max) {
        return (int)(next() % max);
    }
}

public class Generator {
    public static void main(String[] args) {
        int count = 10;
        PrintStream output = System.out;
        
        if (args.length > 0) {
            try {
                count = Integer.parseInt(args[0]);
                if (count <= 0) count = 10;
            } catch (NumberFormatException e) {
                count = 10;
            }
        }
        
        if (args.length > 1) {
            try {
                output = new PrintStream(new FileOutputStream(args[1]));
                System.out.println("Запись в файл: " + args[1]);
            } catch (FileNotFoundException e) {
                System.err.println("Ошибка открытия файла: " + args[1]);
                System.exit(1);
            }
        }
        
        long currentTime = Instant.now().toEpochMilli();
        LCG generator = new LCG(currentTime);
        
        for (int i = 0; i < count; i++) {
            output.println(generator.nextInt(100));
        }
        
        if (args.length > 1) {
            output.close();
            System.out.println("Записано " + count + " чисел в " + args[1]);
        }
    }
}
