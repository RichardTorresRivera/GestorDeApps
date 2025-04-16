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

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)

    def app_exists(self, name):
        return any(app["app_name"] == name for app in self.config)

    def get_available_app_names(self):
        return [app["app_name"] for app in self.config]

    def status_app(self, name):
        for app in self.config:
            if app["app_name"] == name:
                return app["status"]
        return None

    def start_apps(self):
        for app in self.config:
            if app["status"] == "active":
                self.start_app(app)
        time.sleep(1.5)

    def start_app(self, app):
        env = os.environ.copy()
        entry = os.path.join(BASE_DIR, app["entry_point"])
        port = str(app["port"])
        name = app["app_name"]
        print(f"Iniciando {name} en el puerto {port}")
        proc = subprocess.Popen([sys.executable, entry], env=env)
        self.processes[app["app_name"]] = proc
        for app in self.config:
            if app["app_name"] == name:
                app["status"] = "active"
                break
        self.save_config()

    def stop_app(self, name):
        status = self.status_app(name)
        if status == "active":
            print(f"Deteniendo {name}")
            proc = self.processes.get(name)
            if proc:
                proc.terminate()
                proc.wait()
                del self.processes[name]

            # Actualizar self.config y guardar
            for app in self.config:
                if app["app_name"] == name:
                    app["status"] = "stopped"
                    break
            self.save_config()
        elif status == "stopped":
            print(f"La app {name} ya esta detenida")
        elif status == "desactive":
            print(f"La app {name} se encuentra en desarrollo. No acepta comandos de stop y restart")

    def restart_app(self, name):
        for app in self.config:
            if app["app_name"] == name:
                if app["status"] == "desactive":
                    print(f"La app {name} se encuentra en desarrollo. No se puede reiniciar.")
                    return
                if app["status"] == "active":
                    self.stop_app(name)
                self.start_app(app)
                break
        time.sleep(1.5)
        

    def status(self):
        status_list = []
        for app in self.config:
            name = app["app_name"]
            status_list.append({
                "id": app["id"],
                "app_name": name,
                "entry_point": app["entry_point"],
                "port": app["port"],
                "description": app["description"],
                "status": app["status"]
            })
        print(tabulate(status_list, headers="keys", tablefmt="pretty"))

def main():
    manager = AppManager()
    manager.start_apps()
    manager.status()

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
                if not manager.app_exists(name):
                    print(f"La app '{name}' no existe")
                    print("Apps disponibles:", ", ".join(manager.get_available_app_names()))
                else:
                    manager.stop_app(name)
                    manager.status()
        elif cmd_parts[0] == "restart":
            if len(cmd_parts) != 2:
                print("Se supero el numero de argumentos esperados")
                print("Uso correcto: restart <app>")
            else:
                _, name = cmd_parts
                if not manager.app_exists(name):
                    print(f"La app '{name}' no existe")
                    print("Apps disponibles:", ", ".join(manager.get_available_app_names()))
                else:
                    manager.restart_app(name)
                    manager.status()
        elif cmd_parts[0] == "exit":
            print("Finalizando todas las apps...")
            for name in list(manager.processes.keys()):
                manager.stop_app(name)
            break
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    main()
