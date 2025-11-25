public class Car {
        private String ownerName;
        private double carSpeed;
        private double carDirection;
        public Car(String name){
            ownerName=name;
            carSpeed=0;
            carDirection=0;
        }
        public void changeSpeed(double changeValue){
            if(changeValue>0){
                System.out.print("增速");
            }else{
                System.out.print("减速");
            }
            carSpeed+=changeValue;
            double output=Math.abs(changeValue);
            System.out.print(output);
            System.out.println("km/s");
        }
        public void setownerName(String name){
            ownerName=name;
        }
        public String getownerName(){
            return ownerName;
        }
        public void setcarDirection(double angle){
            carDirection=angle;
        }
        public double getcarDirection(){
            return carDirection;
        }
        public void setcarSpeed(double speed){
            carSpeed=speed;
        }
        public double getcarSpeed(){
            return carSpeed;
        }        
        public void stop(){
            carSpeed=0;
            System.out.print("前方已停车");
        }
        public void status(){
            System.out.println("车速："+carSpeed);
            System.out.println("方向:"+carDirection);
        }
    public static void main(String[] args){
    }
}
