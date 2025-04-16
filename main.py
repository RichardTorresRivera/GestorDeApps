import json
import os
import subprocess
import sys
import time
# import threading
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "apps_config.json")

class AppManager:
    def __init__(self):
        self.processes = {}
        self.load_config()

    def load_config(self):
        with open(CONFIG_PATH, "r") as f:
            self.config = json.load(f)

    def start_apps(self):
        for app in self.config:
            if app["status"] == "active":
                self.start_app(app)
        time.sleep(1.5)

    def start_app(self, app):
        env = os.environ.copy()
        entry = os.path.join(BASE_DIR, app["entry_point"])
        port = str(app["port"])
        print(f"Iniciando {app['app_name']} en el puerto {port}")
        proc = subprocess.Popen([sys.executable, entry], env=env)
        self.processes[app["app_name"]] = proc

    def stop_app(self, name):
        proc = self.processes.get(name)
        if proc:
            print(f"Deteniendo {name}")
            proc.terminate()
            proc.wait()
            del self.processes[name]
        else:
            print(f"No se reconoce {name}")

    def restart_app(self, name):
        self.stop_app(name)
        for app in self.config:
            if app["app_name"] == name:
                self.start_app(app)
                break

    def status(self):
        status_list = []
        for app in self.config:
            name = app["app_name"]
            proc = self.processes.get(name)
            status = "active" if proc and proc.poll() is None else "stopped"
            status_list.append({
                "id": app["id"],
                "app_name": name,
                "entry_point": app["entry_point"],
                "port": app["port"],
                "description": app["description"],
                "status": status
            })
        print(tabulate(status_list, headers="keys", tablefmt="pretty"))

def main():
    manager = AppManager()
    manager.start_apps()

    while True:
        cmd = input("Comandos (status, stop <app>, restart <app>, exit): ").strip()
        cmd_parts = cmd.split()
        if not cmd_parts:
            continue
        if cmd_parts[0] == "status":
            if len(cmd_parts) != 1:
                print("status no espera argumentos")
            else:
                manager.status()
        elif cmd_parts[0] == "stop":
            if len(cmd_parts) != 2:
                print("Se supero el numero de argumentos esperados")
                print("Uso correcto: stop <app>")
            else:
                _, name = cmd_parts
                manager.stop_app(name)
        elif cmd_parts[0] == "restart":
            if len(cmd_parts) != 2:
                print("Se supero el numero de argumentos esperados")
                print("Uso correcto: restart <app>")
            else:
                _, name = cmd_parts
                manager.restart_app(name)
        elif cmd_parts[0] == "exit":
            print("Finalizando todas las apps...")
            for name in list(manager.processes.keys()):
                manager.stop_app(name)
            break
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    main()
