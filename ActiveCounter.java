package com.burk;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class ActiveCounter {

    public Random rand = new Random();
    private char bitsOfNumber = 0;
    private char bitsOfExponent = 0;
    private char maxBitsOfNumber = (char)(Math.pow(2,16) - 1);
    private char maxBitsOfExponents = (char)(Math.pow(2,16) - 1);

    public void addone(){
        try {
            if((1 / Math.pow(2, this.bitsOfExponent) > rand.nextDouble())){
                if(this.bitsOfNumber == this.maxBitsOfNumber){
                    this.bitsOfExponent ++;
                    if(this.bitsOfExponent == this.maxBitsOfExponents){
                        System.exit(1);
                    }
                    this.bitsOfNumber = (char)((int)this.bitsOfNumber >> 1);
                }
                else{
                    this.bitsOfNumber ++;
                }
            }
        }
        catch (Exception e){
            System.out.println("Bits overflow.");
        }
    }

    public static void main(String[] args) {
        ActiveCounter ac = new ActiveCounter();
        for(int i = 0; i < 1000000; i++){
            ac.addone();
        }
        int finalResult = (int)(ac.bitsOfNumber * Math.pow(2, ac.bitsOfExponent));
        System.out.println("The final value of the active counter in decimal: "+ finalResult + "");

        try{
            BufferedWriter out = new BufferedWriter(new FileWriter("output3.txt"));
            out.write("The final value of the active counter in decimal: "+ finalResult + "");
            out.close();
        } catch (IOException exception) {
            exception.printStackTrace();
        }
    }
}
