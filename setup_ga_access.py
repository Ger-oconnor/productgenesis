#!/usr/bin/env python3
"""
One-time setup: grants the service account Viewer access to the GA4 property.
Run this once. After it succeeds, refresh_analytics.py works without any browser login.

Usage: python setup_ga_access.py
"""

import json
import os

CLIENT_SECRETS = "C:/Users/geral/Downloads/client_secret_153256688942-fp087vrv067kd0npauh7voqkk4877bov.apps.googleusercontent.com.json"
SERVICE_ACCOUNT_EMAIL = "product-genesis-analytics@product-genesis-analytics.iam.gserviceaccount.com"
PROPERTY_ID = "160712637"
SCOPES = ["https://www.googleapis.com/auth/analytics.manage.users"]

def main():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.analytics.admin import AnalyticsAdminServiceClient
    from google.analytics.admin_v1alpha.types import AccessBinding

    print("Opening browser to sign in with your Google account...")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    creds = flow.run_local_server(port=0)

    client = AnalyticsAdminServiceClient(credentials=creds)
    property_name = f"properties/{PROPERTY_ID}"

    binding = AccessBinding(
        user=SERVICE_ACCOUNT_EMAIL,
        roles=["predefinedRoles/viewer"],
    )

    result = client.create_access_binding(
        parent=property_name,
        access_binding=binding,
    )
    print("\nSuccess! Service account granted Viewer access:")
    print(f"  {result.name}")
    print("\nYou can now run: python refresh_analytics.py")

if __name__ == "__main__":
    main()
