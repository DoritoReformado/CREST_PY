using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        // Especifica la ubicación de la carpeta de entorno virtual de Python
        string pythonEnvPath = @"C:\Users\Jorge\.conda\envs\ArcPython";

        // Comando de Python que deseas ejecutar
        string pythonScript = "suma.py";

        // Crea un proceso para ejecutar Python
        using (Process process = new Process())
        {
            process.StartInfo.FileName = Path.Combine(pythonEnvPath, "Scripts", "python.exe"); // Ruta al ejecutable de Python en el entorno virtual
            process.StartInfo.Arguments = pythonScript; // Script de Python que deseas ejecutar
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.CreateNoWindow = true;

            process.Start();

            // Captura la salida estándar y los errores
            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            process.WaitForExit();

            // Imprime la salida y los errores (o puedes manejarlos de otras formas)
            Console.WriteLine("Salida de Python:");
            Console.WriteLine(output);
            Console.WriteLine("Errores de Python:");
            Console.WriteLine(error);
        }
    }
}
