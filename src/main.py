from changelog_generator import *

if not authenticate():
    print("Authentication failed. Exiting...")
    exit(0)

release_info = get_latest_release()
if not release_info:
    print("No releases found. Exiting...")
    exit(1)
    
latest_version = release_info["latest_version"]
print("Latest version:", latest_version)

merged_prs = get_merged_prs(release_info["latest_release_date"])
if not merged_prs:
    print("No merged PRs found. Exiting...")
    exit(2)
    
new_version = calculate_new_version(latest_version, merged_prs)
if not new_version:
    print("Invalid version format. Exiting...")
    exit(3)
    
print("New version:", new_version)

changelog_entry = f"## {new_version} ({datetime.now().strftime('%Y-%m-%d')})\n"
for pr in merged_prs:
    changelog_entry += f"- {pr.title} (#{pr.number})\n"
    
print("Changelog entry generated:\n", changelog_entry)

if update_changelog(changelog_entry):
    print("Changelog updated successfully.")
else:
    print("Failed to update the changelog.")
    exit(4)