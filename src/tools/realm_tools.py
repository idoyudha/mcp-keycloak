from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
def get_realm_info() -> Dict[str, Any]:
    """
    Get information about the current realm.

    Returns:
        Realm configuration object
    """
    response = client._make_request("GET", "", params=None)
    return response


@mcp.tool()
def update_realm_settings(
    display_name: Optional[str] = None,
    display_name_html: Optional[str] = None,
    login_theme: Optional[str] = None,
    account_theme: Optional[str] = None,
    admin_theme: Optional[str] = None,
    email_theme: Optional[str] = None,
    enabled: Optional[bool] = None,
    registration_allowed: Optional[bool] = None,
    registration_email_as_username: Optional[bool] = None,
    reset_password_allowed: Optional[bool] = None,
    remember_me: Optional[bool] = None,
    verify_email: Optional[bool] = None,
    login_with_email_allowed: Optional[bool] = None,
    duplicate_emails_allowed: Optional[bool] = None,
    ssl_required: Optional[str] = None,
    brute_force_protected: Optional[bool] = None,
    permanent_lockout: Optional[bool] = None,
    max_failure_wait_seconds: Optional[int] = None,
    minimum_quick_login_wait_seconds: Optional[int] = None,
    wait_increment_seconds: Optional[int] = None,
    quick_login_check_milli_seconds: Optional[int] = None,
    max_delta_time_seconds: Optional[int] = None,
    failure_factor: Optional[int] = None,
    default_locale: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update realm settings.

    Args:
        display_name: Display name for the realm
        display_name_html: HTML display name
        login_theme: Login theme name
        account_theme: Account management theme
        admin_theme: Admin console theme
        email_theme: Email theme
        enabled: Whether realm is enabled
        registration_allowed: Allow user registration
        registration_email_as_username: Use email as username
        reset_password_allowed: Allow password reset
        remember_me: Enable remember me
        verify_email: Require email verification
        login_with_email_allowed: Allow login with email
        duplicate_emails_allowed: Allow duplicate emails
        ssl_required: SSL requirement (none, external, all)
        brute_force_protected: Enable brute force protection
        permanent_lockout: Permanent lockout on max failures
        max_failure_wait_seconds: Max wait after failures
        minimum_quick_login_wait_seconds: Min wait between quick logins
        wait_increment_seconds: Wait increment
        quick_login_check_milli_seconds: Quick login check interval
        max_delta_time_seconds: Max time between failures
        failure_factor: Failure factor
        default_locale: Default locale

    Returns:
        Status message
    """
    # Get current realm data
    current_realm = client._make_request("GET", "")

    # Update only provided fields
    if display_name is not None:
        current_realm["displayName"] = display_name
    if display_name_html is not None:
        current_realm["displayNameHtml"] = display_name_html
    if login_theme is not None:
        current_realm["loginTheme"] = login_theme
    if account_theme is not None:
        current_realm["accountTheme"] = account_theme
    if admin_theme is not None:
        current_realm["adminTheme"] = admin_theme
    if email_theme is not None:
        current_realm["emailTheme"] = email_theme
    if enabled is not None:
        current_realm["enabled"] = enabled
    if registration_allowed is not None:
        current_realm["registrationAllowed"] = registration_allowed
    if registration_email_as_username is not None:
        current_realm["registrationEmailAsUsername"] = registration_email_as_username
    if reset_password_allowed is not None:
        current_realm["resetPasswordAllowed"] = reset_password_allowed
    if remember_me is not None:
        current_realm["rememberMe"] = remember_me
    if verify_email is not None:
        current_realm["verifyEmail"] = verify_email
    if login_with_email_allowed is not None:
        current_realm["loginWithEmailAllowed"] = login_with_email_allowed
    if duplicate_emails_allowed is not None:
        current_realm["duplicateEmailsAllowed"] = duplicate_emails_allowed
    if ssl_required is not None:
        current_realm["sslRequired"] = ssl_required
    if brute_force_protected is not None:
        current_realm["bruteForceProtected"] = brute_force_protected
    if permanent_lockout is not None:
        current_realm["permanentLockout"] = permanent_lockout
    if max_failure_wait_seconds is not None:
        current_realm["maxFailureWaitSeconds"] = max_failure_wait_seconds
    if minimum_quick_login_wait_seconds is not None:
        current_realm["minimumQuickLoginWaitSeconds"] = minimum_quick_login_wait_seconds
    if wait_increment_seconds is not None:
        current_realm["waitIncrementSeconds"] = wait_increment_seconds
    if quick_login_check_milli_seconds is not None:
        current_realm["quickLoginCheckMilliSeconds"] = quick_login_check_milli_seconds
    if max_delta_time_seconds is not None:
        current_realm["maxDeltaTimeSeconds"] = max_delta_time_seconds
    if failure_factor is not None:
        current_realm["failureFactor"] = failure_factor
    if default_locale is not None:
        current_realm["defaultLocale"] = default_locale

    client._make_request("PUT", "", data=current_realm)
    return {
        "status": "updated",
        "message": f"Realm {client.realm_name} settings updated successfully",
    }


@mcp.tool()
def get_realm_events_config() -> Dict[str, Any]:
    """
    Get realm events configuration.

    Returns:
        Events configuration object
    """
    return client._make_request("GET", "/events/config")


@mcp.tool()
def update_realm_events_config(
    events_enabled: Optional[bool] = None,
    events_listeners: Optional[List[str]] = None,
    enabled_event_types: Optional[List[str]] = None,
    admin_events_enabled: Optional[bool] = None,
    admin_events_details_enabled: Optional[bool] = None,
) -> Dict[str, str]:
    """
    Update realm events configuration.

    Args:
        events_enabled: Enable events
        events_listeners: Event listener implementations
        enabled_event_types: Types of events to record
        admin_events_enabled: Enable admin events
        admin_events_details_enabled: Include details in admin events

    Returns:
        Status message
    """
    # Get current config
    current_config = client._make_request("GET", "/events/config")

    # Update only provided fields
    if events_enabled is not None:
        current_config["eventsEnabled"] = events_enabled
    if events_listeners is not None:
        current_config["eventsListeners"] = events_listeners
    if enabled_event_types is not None:
        current_config["enabledEventTypes"] = enabled_event_types
    if admin_events_enabled is not None:
        current_config["adminEventsEnabled"] = admin_events_enabled
    if admin_events_details_enabled is not None:
        current_config["adminEventsDetailsEnabled"] = admin_events_details_enabled

    client._make_request("PUT", "/events/config", data=current_config)
    return {"status": "updated", "message": "Events configuration updated successfully"}


@mcp.tool()
def get_realm_default_groups() -> List[Dict[str, Any]]:
    """
    Get default groups for the realm.

    Returns:
        List of default groups
    """
    return client._make_request("GET", "/default-groups")


@mcp.tool()
def add_realm_default_group(group_id: str) -> Dict[str, str]:
    """
    Add a default group to the realm.

    Args:
        group_id: Group ID to add as default

    Returns:
        Status message
    """
    client._make_request("PUT", f"/default-groups/{group_id}")
    return {"status": "added", "message": f"Group {group_id} added as default group"}


@mcp.tool()
def remove_realm_default_group(group_id: str) -> Dict[str, str]:
    """
    Remove a default group from the realm.

    Args:
        group_id: Group ID to remove from defaults

    Returns:
        Status message
    """
    client._make_request("DELETE", f"/default-groups/{group_id}")
    return {
        "status": "removed",
        "message": f"Group {group_id} removed from default groups",
    }


@mcp.tool()
def remove_all_user_sessions() -> Dict[str, str]:
    """
    Remove all sessions for a user.

    Args:
        user_id: User ID to remove sessions for

    Returns:
        Status message
    """
    client._make_request("POST", "/logout-all")
    return {
        "status": "removed",
        "message": "Sessions for all users removed successfully",
    }
