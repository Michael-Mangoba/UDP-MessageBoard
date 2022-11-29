import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketException;
  
public class chatServer
{
    public static void main(String[] args) throws IOException
    {
        // Step 1 : Create a socket to listen at port 1234
        InetAddress newIp = InetAddress.getLocalHost();
        DatagramSocket ds = new DatagramSocket(1234);
        byte[] receive = new byte[65535];

        byte buf[] = null;
        System.out.println(newIp);
        DatagramPacket DpReceive = null;
        while (true)
        {
          // Step 2 : create a DatgramPacket to receive the data.
            DpReceive = new DatagramPacket(receive, receive.length);
  
            // Step 3 : revieve the data in byte buffer.
            ds.receive(DpReceive);
            if(data(receive).equals("/join")){
                buf = "Connection to the Message Board Server is successful!".getBytes();
                DatagramPacket DpSend = new DatagramPacket(buf, buf.length, newIp, 1234);
                ds.send(DpSend);
            }
            System.out.println("Client:-" + data(receive));
  
            // Exit the server if the client sends "bye"
            if (data(receive).toString().equals("bye"))
            {
                System.out.println("Client sent bye.....EXITING");
                ds.close();
                break;
            }
  
            // Clear the buffer after every message.
            receive = new byte[65535];
        }
    }
  
    // A utility method to convert the byte array
    // data into a string representation.
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