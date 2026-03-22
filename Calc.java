import java.util.*;
class Calc{
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        float x, y, z;
        int choice;

        System.out.println("Enter First Number: ");
        x = input.nextFloat();
        System.out.println("Enter Second Number: ");
        y = input.nextFloat();

        System.out.println("Select \n 1. For Addition \n 2. For Subsraction \n 3. For Multiplicatio \n 4. Division");
        choice = input.nextInt();


        if (choice == 1){
            System.out.println(x + y);
        }
        else if (choice == 2) {
            System.out.println(x-y);
        }
        else if(choice == 3){
            System.out.println(x * y);
        }
        else if (choice == 4){
            System.out.println(x / y);
        }
        else{
            System.out.println("Error")
        }

    }
}