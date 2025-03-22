import os
import subprocess

def create_task_from_xml(task_name, xml_file_path):
    """
    Creates a task using XML file and schtasks.exe.
    """
    user_home = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(user_home, "run_script.bat")

    xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-03-21T10:00:00</Date>
    <Author>{os.getlogin()}</Author>
    <Description>{task_name} - Created from XML</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>{os.getlogin()}</UserId>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{os.getlogin()}</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{script_path}</Command>
    </Exec>
  </Actions>
</Task>
"""
    with open(xml_file_path, "w", encoding="utf-16") as f:
        f.write(xml_content)

    command = [
        "schtasks", "/create", "/tn", task_name,
        "/xml", xml_file_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"✅ Task '{task_name}' created successfully from XML.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating task from XML: {e}")
    except FileNotFoundError:
        print("❌ Error: schtasks.exe not found. Ensure you're running this on Windows.")

if __name__ == "__main__":
    if os.name != "nt":
        print("❌ This script only works on Windows.")
        exit(1)
    
    task_name = "MonitorLogin"
    xml_file_path = os.path.join(os.path.expanduser("~"), "task_definition.xml")
    create_task_from_xml(task_name, xml_file_path)
