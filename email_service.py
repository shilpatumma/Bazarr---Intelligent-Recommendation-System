"""
email_service.py — Beautiful HTML Email Sender
================================================
Uses Gmail SMTP (free). Setup:
  1. Go to https://myaccount.google.com/apppasswords
  2. Generate an App Password (need 2FA enabled on Gmail)
  3. Fill SENDER_EMAIL and SENDER_PASSWORD below
"""

import smtplib, ssl, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ── CONFIG — Fill these with your Gmail details ────────────────────────────
SENDER_EMAIL    = "lily.atoz123@gmail.com"      # ← apna Gmail yahan
SENDER_PASSWORD = "jtvh urqs vzxc xkqo"       # ← Gmail App Password (16 chars)
SENDER_NAME     = "BAZARR"
# ───────────────────────────────────────────────────────────────────────────


def send_email_async(to_email, subject, html_body):
    """Send email in background thread so app doesn't slow down."""
    def _send():
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From']    = f"{SENDER_NAME} <{SENDER_EMAIL}>"
            msg['To']      = to_email
            msg.attach(MIMEText(html_body, 'html'))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            print(f"[Email] ✅ Sent to {to_email}")
        except Exception as e:
            print(f"[Email] ❌ Failed: {e}")

    threading.Thread(target=_send, daemon=True).start()


# ── EMAIL TEMPLATES ────────────────────────────────────────────────────────

def _base_template(content_html):
    """Wraps content in branded email shell."""
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);">

        <!-- HEADER -->
        <tr>
          <td style="background:#000;padding:28px 40px;text-align:center;">
            <h1 style="margin:0;color:#fff;font-size:28px;letter-spacing:6px;font-weight:900;font-family:Arial Black,sans-serif;">BAZARR</h1>
            <p style="margin:4px 0 0;color:#aaa;font-size:11px;letter-spacing:3px;">SHOP SMARTER</p>
          </td>
        </tr>

        <!-- CONTENT -->
        <tr><td style="padding:40px;">
          {content_html}
        </td></tr>

        <!-- FOOTER -->
        <tr>
          <td style="background:#f9f9f9;padding:24px 40px;text-align:center;border-top:1px solid #eee;">
            <p style="margin:0;font-size:12px;color:#aaa;">© {datetime.now().year} Bazarr. All rights reserved.</p>
            <p style="margin:8px 0 0;font-size:11px;color:#ccc;">This email was sent because you registered on Bazarr.</p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_welcome_email(to_email, name, user_id, joined_date):
    """Beautiful welcome email after signup with account details."""
    subject = f"Welcome to Bazarr, {name}! 🎉 Your account is ready"

    content = f"""
    <!-- Welcome banner -->
    <div style="text-align:center;margin-bottom:32px;">
      <div style="width:72px;height:72px;background:#000;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:32px;margin-bottom:16px;">
        🎉
      </div>
      <h2 style="margin:0;font-size:26px;color:#111;font-weight:900;">Welcome aboard, {name}!</h2>
      <p style="margin:8px 0 0;color:#888;font-size:15px;">Your Bazarr account has been created successfully.</p>
    </div>

    <!-- Account details card -->
    <div style="background:#f8f8f8;border-radius:8px;padding:24px;margin-bottom:28px;border-left:4px solid #000;">
      <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:2px;color:#888;text-transform:uppercase;">Your Account Details</p>

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;">
            <span style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Account ID</span>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">
            <span style="font-size:14px;color:#111;font-weight:700;font-family:monospace;background:#fff;padding:3px 10px;border-radius:4px;border:1px solid #ddd;">#{user_id:05d}</span>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;">
            <span style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Name</span>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">
            <span style="font-size:14px;color:#111;font-weight:600;">{name}</span>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;">
            <span style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Email (Login ID)</span>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">
            <span style="font-size:14px;color:#111;">{to_email}</span>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;">
            <span style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Password</span>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">
            <span style="font-size:14px;color:#111;font-family:monospace;background:#fff;padding:3px 10px;border-radius:4px;border:1px solid #ddd;">••••••••</span>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;">
            <span style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:1px;">Member Since</span>
          </td>
          <td style="padding:8px 0;text-align:right;">
            <span style="font-size:14px;color:#111;">{joined_date}</span>
          </td>
        </tr>
      </table>
    </div>

    <!-- What you can do -->
    <p style="margin:0 0 16px;font-size:11px;font-weight:700;letter-spacing:2px;color:#888;text-transform:uppercase;">What you can do now</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
      <tr>
        <td style="padding:10px;background:#f8f8f8;border-radius:6px;margin-bottom:8px;width:48%;">
          <p style="margin:0;font-size:13px;">🛍️ <strong>Browse Products</strong></p>
          <p style="margin:4px 0 0;font-size:12px;color:#888;">Explore thousands of items</p>
        </td>
        <td style="width:4%;"></td>
        <td style="padding:10px;background:#f8f8f8;border-radius:6px;width:48%;">
          <p style="margin:0;font-size:13px;">❤️ <strong>Wishlist</strong></p>
          <p style="margin:4px 0 0;font-size:12px;color:#888;">Save items for later</p>
        </td>
      </tr>
      <tr><td colspan="3" style="height:8px;"></td></tr>
      <tr>
        <td style="padding:10px;background:#f8f8f8;border-radius:6px;width:48%;">
          <p style="margin:0;font-size:13px;">🤖 <strong>Smart Recommendations</strong></p>
          <p style="margin:4px 0 0;font-size:12px;color:#888;">AI-powered suggestions</p>
        </td>
        <td style="width:4%;"></td>
        <td style="padding:10px;background:#f8f8f8;border-radius:6px;width:48%;">
          <p style="margin:0;font-size:13px;">📦 <strong>Track Orders</strong></p>
          <p style="margin:4px 0 0;font-size:12px;color:#888;">Real-time order status</p>
        </td>
      </tr>
    </table>

    <!-- CTA button -->
    <div style="text-align:center;margin-bottom:24px;">
      <a href="http://localhost:5000" style="display:inline-block;background:#000;color:#fff;padding:14px 44px;border-radius:4px;text-decoration:none;font-size:14px;font-weight:700;letter-spacing:2px;">START SHOPPING</a>
    </div>

    <p style="margin:0;font-size:13px;color:#aaa;text-align:center;">
      Keep your login credentials safe. Bazarr will never ask for your password via email.
    </p>
    """

    send_email_async(to_email, subject, _base_template(content))


def send_login_alert_email(to_email, name, login_time):
    """Alert email when user logs in."""
    subject = f"New login to your Bazarr account"

    content = f"""
    <div style="text-align:center;margin-bottom:28px;">
      <div style="font-size:48px;margin-bottom:12px;">🔐</div>
      <h2 style="margin:0;font-size:22px;color:#111;font-weight:900;">New Login Detected</h2>
      <p style="margin:8px 0 0;color:#888;">Hi {name}, we noticed a login to your account.</p>
    </div>

    <div style="background:#f8f8f8;border-radius:8px;padding:24px;margin-bottom:28px;border-left:4px solid #000;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="padding:8px 0;border-bottom:1px solid #eee;">
            <span style="font-size:12px;color:#888;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Account</span>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">
            <span style="font-size:14px;color:#111;">{to_email}</span>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;">
            <span style="font-size:12px;color:#888;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Login Time</span>
          </td>
          <td style="padding:8px 0;text-align:right;">
            <span style="font-size:14px;color:#111;">{login_time}</span>
          </td>
        </tr>
      </table>
    </div>

    <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:6px;padding:16px;margin-bottom:24px;">
      <p style="margin:0;font-size:13px;color:#f57c00;">
        ⚠️ <strong>Not you?</strong> If you did not log in, please change your password immediately.
      </p>
    </div>

    <div style="text-align:center;">
      <a href="http://localhost:5000/profile" style="display:inline-block;background:#000;color:#fff;padding:12px 36px;border-radius:4px;text-decoration:none;font-size:13px;font-weight:700;letter-spacing:2px;">GO TO MY ACCOUNT</a>
    </div>
    """

    send_email_async(to_email, subject, _base_template(content))


def send_order_confirmation_email(to_email, name, order_id, items, total, address):
    """Order placed confirmation email."""
    subject = f"Order #{order_id:05d} Confirmed — Bazarr 🛍️"

    items_html = ""
    for item in items:
        items_html += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #f0f0f0;">
            <span style="font-size:14px;color:#111;">{item["name"]}</span>
            <span style="font-size:12px;color:#888;"> × {item["qty"]}</span>
          </td>
          <td style="padding:10px 0;border-bottom:1px solid #f0f0f0;text-align:right;">
            <span style="font-size:14px;color:#111;font-weight:600;">₹{item["price"]:,.0f}</span>
          </td>
        </tr>"""

    content = f"""
    <div style="text-align:center;margin-bottom:28px;">
      <div style="font-size:48px;margin-bottom:12px;">✅</div>
      <h2 style="margin:0;font-size:24px;color:#111;font-weight:900;">Order Confirmed!</h2>
      <p style="margin:8px 0 0;color:#888;">Thank you {name}, your order is being processed.</p>
      <p style="margin:8px 0 0;font-size:18px;font-weight:700;color:#000;">Order #{order_id:05d}</p>
    </div>

    <div style="background:#f8f8f8;border-radius:8px;padding:24px;margin-bottom:24px;">
      <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:2px;color:#888;text-transform:uppercase;">Order Summary</p>
      <table width="100%" cellpadding="0" cellspacing="0">
        {items_html}
        <tr>
          <td style="padding:14px 0 0;"><span style="font-size:15px;font-weight:900;color:#000;">TOTAL</span></td>
          <td style="padding:14px 0 0;text-align:right;"><span style="font-size:18px;font-weight:900;color:#000;">₹{total:,.0f}</span></td>
        </tr>
      </table>
    </div>

    <div style="background:#f8f8f8;border-radius:8px;padding:20px;margin-bottom:24px;">
      <p style="margin:0 0 8px;font-size:11px;font-weight:700;letter-spacing:2px;color:#888;text-transform:uppercase;">Delivery Address</p>
      <p style="margin:0;font-size:14px;color:#333;line-height:1.6;">{address}</p>
    </div>

    <div style="text-align:center;">
      <a href="http://localhost:5000/orders" style="display:inline-block;background:#000;color:#fff;padding:13px 40px;border-radius:4px;text-decoration:none;font-size:13px;font-weight:700;letter-spacing:2px;">TRACK MY ORDER</a>
    </div>
    """

    send_email_async(to_email, subject, _base_template(content))