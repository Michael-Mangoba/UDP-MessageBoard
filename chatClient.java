import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketException;
import java.util.*;

public class chatClient
{
    public static String Address;
    public static Integer Port;
    public static void main(String args[]) throws IOException {
        Scanner sc = new Scanner(System.in);
        // carrying the data.
        DatagramSocket ds = new DatagramSocket();
  
        InetAddress ip = InetAddress.getByName(Address);
        byte buf[] = null;
  
        DatagramPacket DpReceive = null;

        byte[] receive = new byte[65535];
        // loop while user not enters "bye"
        while (true)
        {
            String inp = sc.nextLine();
  
            String[] command = inp.split(" ");
            if(command[0].equals("/join")){
                connect(command);
                buf = command[0].getBytes();
                DatagramPacket DpSend =
                  new DatagramPacket(buf, buf.length, ip, Port);
                ds.send(DpSend);

                DpReceive = new DatagramPacket(receive, receive.length);
                ds.receive(DpReceive);
                System.out.println("Server: " + data(receive));
            }
            // convert the String input into the byte array.

            // break the loop if user enters "bye"
            if (inp.equals("bye"))
                break;
        }
    }

    private static void connect(String[] input){
        Address = input[1];
        Port = Integer.parseInt(input[2]);
    }

    public static StringBuilder data(byte[] a)
    {
        if (a == null)
            return null;
        StringBuilder ret = new StringBuilder();
        int i = 0;
        while (a[i] != 0)
        {
            ret.append((char) a[i]);
            i++;
        }
        return ret;
    }
}