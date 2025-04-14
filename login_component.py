# login_component.py
import streamlit.components.v1 as components

def google_login():
    # Replace YOUR_GOOGLE_CLIENT_ID with your actual Client ID from Google Cloud Console.
    html_code = """
    <html>
    <head>
      <meta name="google-signin-client_id" content="YOUR_GOOGLE_CLIENT_ID">
      <script src="https://accounts.google.com/gsi/client" async defer></script>
    </head>
    <body>
      <!-- The div below renders the Google Sign-In button -->
      <div id="g_id_onload"
           data-client_id="YOUR_GOOGLE_CLIENT_ID"
           data-context="signin"
           data-ux_mode="popup"
           data-callback="handleCredentialResponse"
           data-auto_prompt="false">
      </div>
      <div class="g_id_signin"
           data-type="standard"
           data-shape="rectangular"
           data-theme="outline"
           data-text="sign_in_with"
           data-size="large"
           data-logo_alignment="left">
      </div>
      <script>
        function handleCredentialResponse(response) {
          // Redirect with the JWT token as a query parameter.
          window.location.href = "?token=" + response.credential;
        }
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=400)
