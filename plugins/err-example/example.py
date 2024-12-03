from errbot import BotPlugin, botcmd
import paramiko
import subprocess


class TelegramFeatures(BotPlugin):
    """
    This plugin provides multiple advanced features, including a menu system
    and commands for server interactions via SSH.
    """

    SERVER_IP = "192.168.1.21"
    SERVER_USERNAME = "kali"
    SSH_KEY_PATH = "/home/zulfix/.ssh/errbot_key"  # Path to your SSH private key

    @botcmd
    def halotrinix(self, msg, args):
        """
        Respond with a greeting and display a menu of options in a friendly format with direct commands.
        """
        user_name = msg.frm.username or "Kak"
        greeting = (
            f"Selamat pagi 🌞!!\n"
            f"Kak {user_name} terhubung dengan HaloTrinix.\n\n"
            "Silakan pilih opsi di bawah terlebih dahulu ya kak:\n"
        )
        menu = (
            "1️⃣ Run Traceroute ke Target\n"
            "   👉 Ketik: /traceroute <target>\n\n"
            "2️⃣ Cek Koneksi Server\n"
            "   👉 Ketik: /check_server\n\n"
            "3️⃣ Lihat Uptime Server via SSH\n"
            "   👉 Ketik: /server_uptime\n\n"
            "4️⃣ Keluar\n"
            "   👉 Ketik: /exit\n"
        )
        return f"{greeting}{menu}"

    @botcmd
    def traceroute(self, msg, args):
        """
        Run traceroute to a specified target.
        Usage: /traceroute <target>
        """
        target = args.strip()
        if not target:
            return "Silakan berikan target, contohnya: `/traceroute 8.8.8.8`."
        try:
            output = subprocess.check_output(["traceroute", target], text=True)
            return f"Traceroute ke {target}:\n```\n{output}\n```"
        except Exception as e:
            return f"Terjadi kesalahan saat menjalankan traceroute: {str(e)}"

    @botcmd
    def check_server(self, msg, args):
        """
        Check the server's connectivity using SSH.
        Usage: /check_server
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.SERVER_IP,
                username=self.SERVER_USERNAME,
                key_filename=self.SSH_KEY_PATH
            )
            ssh.close()
            return f"✅ Server {self.SERVER_IP} dapat diakses melalui SSH."
        except Exception as e:
            return f"Terjadi kesalahan saat menghubungkan ke server: {str(e)}"

    @botcmd
    def server_uptime(self, msg, args):
        """
        Get the server's uptime using SSH.
        Usage: /server_uptime
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.SERVER_IP,
                username=self.SERVER_USERNAME,
                key_filename=self.SSH_KEY_PATH
            )

            stdin, stdout, stderr = ssh.exec_command("uptime")
            uptime = stdout.read().decode().strip()
            ssh.close()

            return f"📊 Uptime server:\n```\n{uptime}\n```"
        except Exception as e:
            return f"Terjadi kesalahan saat mendapatkan uptime server: {str(e)}"
