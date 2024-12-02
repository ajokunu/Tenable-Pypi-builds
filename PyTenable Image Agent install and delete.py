#!/usr/bin/env python3

from tenable.io import TenableIO
import subprocess
import time
from datetime import datetime
import sys

class TenableGoldenImageAgent:
    def __init__(self):
        self.access_key = "YOUR_ACCESS_KEY" # This is going to be on the Tenable.io account or generated through documentation
        self.secret_key = "YOUR_SECRET_KEY" # same as above
        self.email_recipient = "your.email@company.com" # send results in whatever format to this email
        self.tio = TenableIO(self.access_key, self.secret_key) 
        
        # Single audit template ID for your compliance policy, you can get this through the API check docs
        self.audit_template_id = "YOUR_AUDIT_TEMPLATE_ID"
        
    def install_agent(self): 
        """Install Tenable agent using the gui provided curl command"""
        print("Installing Tenable agent onto Golden Image for testing")
        install_command = """
        curl -H 'X-Key: 6055ebc258af197568f63ebb8e96981b5d1077229b3e7f0b2c03df42ac8cdc12' \
        'https://sensor.cloud.tenable.com/install/agent?name=agent-name&groups=Golden Image Pipeline' | bash
        """ 
        try:
            subprocess.run(install_command, shell=True, check=True) # testing if our install went through
            print("Agent installation was successful, next step is to scan with agent once plugins are loaded")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing agent, please check the log files on the os or consult Tenable documentation: {e}")
            return False

    def create_and_launch_scan(self):
        """Creates and launchs a new scan using pyTenable, make sure pytenable is installed or this wont work"""
        try:
            scan = self.tio.scans.create(
                name=f"Compliance Scan {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                template=self.audit_template_id,
                targets=['localhost'], # dont need to specify when using an agent
                credentials={'agent_group_id': ["Golden Image Pipeline"]}
            )
            scan.launch()
            print(f"Scan created and launched with ID: {scan.id}") #api tests should work here to verify if their is a problem
            return scan
        except Exception as e:
            print(f"Error creating/launching scan: {e}")
            return None

    def check_scan_status(self, scan):
        """Check scan status using pyTenable"""
        try:
            scan.download()
            status = scan.status()
            print(f"Current scan status: {status}")
            return status
        except Exception as e:
            print(f"Error checking scan status: {e}")
            return None

    def export_results(self, scan):
        """Export scan results using pyTenable"""
        try:
            scan.download()
            export = scan.export_scan(
                format='pdf',
                chapters='vuln_by_host', # Change to audits if doing a compliance Audit scan
                recipients=[self.email_recipient] # defined above dont change this value to your email
            )
            print(f"Results exported successfully to {self.email_recipient}")
            return True
        except Exception as e:
            print(f"Error exporting results: {e}")
            return False

    def uninstall_agent(self): # This works half the time so far, windows should work...
        """Uninstall the Tenable agent"""
        uninstall_command = 'sudo /opt/nessus_agent/sbin/nessuscli agent unlink && sudo /etc/init.d/nessusagent stop && sudo apt-get remove nessus-agent -y'
        try:
            subprocess.run(uninstall_command, shell=True, check=True)
            print("Agent uninstalled successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error uninstalling agent: {e}")
            return False

    def run_workflow(self): # checks to make the full script works 
        """Execute the complete workflow"""
        if not self.install_agent():
            return False
        
        print("Waiting 60 seconds for agent to register...") # adjust this if their is an issue with agent registration creating a timeout
        time.sleep(60)
        
        scan = self.create_and_launch_scan()
        if not scan:
            return False
        
        print("Waiting for scan to complete...")
        while True:
            status = self.check_scan_status(scan)
            if status == 'completed':
                break
            elif status in ['error', 'canceled']:
                print(f"Scan failed with status: {status}")
                return False
            time.sleep(120)
        
        if not self.export_results(scan):
            return False
        
        if not self.uninstall_agent():
            return False
        
        print("Workflow completed successfully, verify the results are delivered as expected within 5 minutes before running again.")
        return True

if __name__ == "__main__":
    scanner = TenableGoldenImageAgent()
    if not scanner.run_workflow():
        sys.exit(1)