#!/usr/bin/env python3
"""Submit a runtime-safe True Shuffle patch to EeveeSpotifyRevivedPublic.

This is intentionally self-contained so the GitHub Action can use the stored
BOUNTY_GITHUB_TOKEN to create/update a fork branch and open the upstream PR.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UPSTREAM_OWNER = "Meeep1"
REPO = "EeveeSpotifyRevivedPublic"
UPSTREAM = f"{UPSTREAM_OWNER}/{REPO}"
BRANCH = "codex/true-shuffle-runtime-safe"
ISSUE_NUMBER = 11

TOKEN = os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("BOUNTY_GITHUB_TOKEN is required")

API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "bounty-autopilot-true-shuffle-submitter",
}


def request(method: str, endpoint: str, data: dict | None = None, ok=(200, 201, 202, 204)):
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(API + endpoint, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            if resp.status not in ok:
                raise RuntimeError(f"Unexpected status {resp.status} for {method} {endpoint}: {raw}")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        if exc.code in ok:
            return json.loads(raw) if raw else None
        raise RuntimeError(f"GitHub API {method} {endpoint} failed: {exc.code} {raw}") from exc


def request_or_none(method: str, endpoint: str, data: dict | None = None):
    try:
        return request(method, endpoint, data=data)
    except RuntimeError as exc:
        if "failed: 404" in str(exc):
            return None
        raise


def contents_path(path: str) -> str:
    return urllib.parse.quote(path, safe="")


def fetch_text(owner: str, repo: str, path: str, ref: str = "main") -> str:
    item = request("GET", f"/repos/{owner}/{repo}/contents/{contents_path(path)}?ref={urllib.parse.quote(ref, safe='')}")
    return base64.b64decode(item["content"]).decode("utf-8")


def patch_tweak(text: str) -> str:
    if "TrueShuffleHookInstaller.installIfEnabled()" in text:
        return text
    text = text.replace(
        "            if UserDefaults.patchType.isPatching {\n                BasePremiumPatchingGroup().activate()\n            }",
        "            if UserDefaults.patchType.isPatching {\n                BasePremiumPatchingGroup().activate()\n                TrueShuffleHookInstaller.installIfEnabled()\n            }",
        1,
    )
    text = text.replace(
        "        if UserDefaults.patchType.isPatching {\n            activatePremiumPatchingGroup()\n        }",
        "        if UserDefaults.patchType.isPatching {\n            activatePremiumPatchingGroup()\n            TrueShuffleHookInstaller.installIfEnabled()\n        }",
        1,
    )
    return text


def patch_settings(text: str) -> str:
    if "@State var trueShuffleEnabled" not in text:
        text = text.replace(
            "    @State var overwriteConfiguration = UserDefaults.overwriteConfiguration\n",
            "    @State var overwriteConfiguration = UserDefaults.overwriteConfiguration\n"
            "    @State var trueShuffleEnabled = UserDefaults.trueShuffleEnabled\n",
            1,
        )

    if ".onChange(of: trueShuffleEnabled)" not in text:
        text = text.replace(
            "            .onChange(of: overwriteConfiguration) { overwriteConfiguration in\n"
            "                UserDefaults.overwriteConfiguration = overwriteConfiguration\n"
            "                OfflineHelper.resetData()\n"
            "            }\n",
            "            .onChange(of: overwriteConfiguration) { overwriteConfiguration in\n"
            "                UserDefaults.overwriteConfiguration = overwriteConfiguration\n"
            "                OfflineHelper.resetData()\n"
            "            }\n"
            "\n"
            "            .onChange(of: trueShuffleEnabled) { isEnabled in\n"
            "                UserDefaults.trueShuffleEnabled = isEnabled\n"
            "            }\n",
            1,
        )

    if "enable_true_shuffle" not in text:
        overwrite_section = (
            "                Section(\n"
            "                    footer: Text(\"overwrite_configuration_description\".localized)\n"
            "                ) {\n"
            "                    Toggle(\n"
            "                        \"overwrite_configuration\".localized,\n"
            "                        isOn: $overwriteConfiguration\n"
            "                    )\n"
            "                }"
        )
        true_shuffle_section = (
            "\n\n"
            "                Section(\n"
            "                    footer: Text(\n"
            "                        \"true_shuffle_description\"\n"
            "                            .localizeWithFormat(\"restart_is_required_description\".localized)\n"
            "                    )\n"
            "                ) {\n"
            "                    Toggle(\n"
            "                        \"enable_true_shuffle\".localized,\n"
            "                        isOn: $trueShuffleEnabled\n"
            "                    )\n"
            "                }"
        )
        text = text.replace(overwrite_section, overwrite_section + true_shuffle_section, 1)
    return text


def patch_user_defaults(text: str) -> str:
    if "trueShuffleEnabledKey" not in text:
        text = text.replace(
            "    private static let patchTypeKey = \"patchType\"\n",
            "    private static let patchTypeKey = \"patchType\"\n"
            "    private static let trueShuffleEnabledKey = \"trueShuffleEnabled\"\n",
            1,
        )
    if "static var trueShuffleEnabled" not in text:
        text = text.replace(
            "    static var overwriteConfiguration: Bool {\n",
            "    static var trueShuffleEnabled: Bool {\n"
            "        get {\n"
            "            container.object(forKey: trueShuffleEnabledKey) as? Bool ?? true\n"
            "        }\n"
            "        set (isEnabled) {\n"
            "            container.set(isEnabled, forKey: trueShuffleEnabledKey)\n"
            "        }\n"
            "    }\n"
            "    \n"
            "    static var overwriteConfiguration: Bool {\n",
            1,
        )
    return text


def patch_localizable(text: str) -> str:
    if "enable_true_shuffle" in text:
        return text
    return text.replace(
        "overwrite_configuration_description = \"Replace remote configuration with the dumped Premium one. This configuration defines most UI/UX parameters and may be helpful, although it could cause issues.\";\n\n",
        "overwrite_configuration_description = \"Replace remote configuration with the dumped Premium one. This configuration defines most UI/UX parameters and may be helpful, although it could cause issues.\";\n\n"
        "enable_true_shuffle = \"Enable True Shuffle\";\n"
        "true_shuffle_description = \"Disables Spotify's weighted recommendation shuffle path so playlist shuffles keep the original randomized track list instead of injected recommendations. %@\";\n\n",
        1,
    )


def true_shuffle_file() -> str:
    return r'''import Foundation
import ObjectiveC.runtime

enum TrueShuffleHookInstaller {
    private static var didInstall = false
    private static var retryTimer: Timer?
    private static var retryCount = 0
    private static let maxRetryCount = 20

    private typealias WeightForTrackIMP = @convention(c) (
        AnyObject,
        Selector,
        AnyObject,
        Bool,
        Bool
    ) -> Double

    static func installIfEnabled() {
        guard UserDefaults.trueShuffleEnabled else {
            writeDebugLog("True Shuffle is disabled in settings; skipping hook install")
            return
        }

        DispatchQueue.main.async {
            retryCount = 0
            retryTimer?.invalidate()
            retryTimer = nil

            if installWhenAvailable() {
                return
            }

            retryTimer = Timer.scheduledTimer(withTimeInterval: 1.5, repeats: true) { timer in
                retryCount += 1

                if installWhenAvailable() || retryCount >= maxRetryCount {
                    timer.invalidate()
                    retryTimer = nil

                    if !didInstall {
                        writeDebugLog("True Shuffle: no compatible shuffle class found after retries")
                    }
                }
            }
        }
    }

    private static func installWhenAvailable() -> Bool {
        guard !didInstall else { return true }

        let weightSelector = NSSelectorFromString("weightForTrack:recommendedTrack:mergedList:")
        let weightedListSelector = NSSelectorFromString("weightedShuffleListWithTracks:recommendations:")

        if let knownClass = NSClassFromString("SPTFreeTierPlaylistTrackShuffler"),
           install(on: knownClass, weightSelector: weightSelector, weightedListSelector: weightedListSelector) {
            return true
        }

        var classCount: UInt32 = 0
        guard let classes = objc_copyClassList(&classCount) else {
            writeDebugLog("True Shuffle: failed to enumerate Objective-C classes")
            return false
        }
        defer { free(classes) }

        for index in 0 ..< Int(classCount) {
            let cls = classes[index]
            let className = NSStringFromClass(cls).lowercased()

            guard className.contains("shuffle") || className.contains("shuffler") else {
                continue
            }

            if install(on: cls, weightSelector: weightSelector, weightedListSelector: weightedListSelector) {
                return true
            }
        }

        return false
    }

    private static func install(
        on cls: AnyClass,
        weightSelector: Selector,
        weightedListSelector: Selector
    ) -> Bool {
        guard let weightMethod = class_getInstanceMethod(cls, weightSelector) else {
            return false
        }

        let originalWeightIMP = method_getImplementation(weightMethod)

        let weightBlock: @convention(block) (AnyObject, AnyObject, Bool, Bool) -> Double = {
            object,
            track,
            _,
            _
            in
            let original = unsafeBitCast(originalWeightIMP, to: WeightForTrackIMP.self)
            return original(object, weightSelector, track, false, false)
        }

        method_setImplementation(weightMethod, imp_implementationWithBlock(weightBlock as Any))

        if let weightedListMethod = class_getInstanceMethod(cls, weightedListSelector) {
            let weightedListBlock: @convention(block) (AnyObject, AnyObject, AnyObject) -> AnyObject? = {
                _,
                tracks,
                _
                in
                tracks
            }

            method_setImplementation(weightedListMethod, imp_implementationWithBlock(weightedListBlock as Any))
        }

        didInstall = true
        retryTimer?.invalidate()
        retryTimer = nil
        writeDebugLog("True Shuffle hooks installed on class: \(NSStringFromClass(cls))")
        return true
    }
}
'''


def changed_files() -> dict[str, str]:
    owner, repo = UPSTREAM_OWNER, REPO
    files = {
        "Sources/EeveeSpotify/Tweak.x.swift": patch_tweak(fetch_text(owner, repo, "Sources/EeveeSpotify/Tweak.x.swift")),
        "Sources/EeveeSpotify/Settings/Sections/Patching/Views/EeveePatchingSettingsView.swift": patch_settings(fetch_text(owner, repo, "Sources/EeveeSpotify/Settings/Sections/Patching/Views/EeveePatchingSettingsView.swift")),
        "Sources/EeveeSpotify/Shared/Models/Extensions/UserDefaults+Extension.swift": patch_user_defaults(fetch_text(owner, repo, "Sources/EeveeSpotify/Shared/Models/Extensions/UserDefaults+Extension.swift")),
        "layout/Library/Application Support/EeveeSpotify.bundle/en.lproj/Localizable.strings": patch_localizable(fetch_text(owner, repo, "layout/Library/Application Support/EeveeSpotify.bundle/en.lproj/Localizable.strings")),
        "Sources/EeveeSpotify/Premium/TrueShuffle.x.swift": true_shuffle_file(),
    }
    return files


def ensure_fork(login: str) -> dict:
    fork = request_or_none("GET", f"/repos/{login}/{REPO}")
    if fork:
        return fork

    print(f"Creating fork {login}/{REPO} from {UPSTREAM}...")
    try:
        request("POST", f"/repos/{UPSTREAM}/forks", ok=(200, 201, 202))
    except RuntimeError as exc:
        if "already exists" not in str(exc).lower():
            raise

    for _ in range(24):
        fork = request_or_none("GET", f"/repos/{login}/{REPO}")
        if fork:
            return fork
        time.sleep(5)
    raise RuntimeError(f"Timed out waiting for fork {login}/{REPO}")


def open_or_update_pr(login: str, head_sha: str) -> str:
    query = urllib.parse.urlencode({"state": "open", "head": f"{login}:{BRANCH}"})
    prs = request("GET", f"/repos/{UPSTREAM}/pulls?{query}")
    if prs:
        print(f"Existing PR: {prs[0]['html_url']}")
        return prs[0]["html_url"]

    body = f"""Fixes #{ISSUE_NUMBER}.

This adds an optional True Shuffle toggle and a runtime-safe installer for Spotify's free-tier playlist shuffler path.

What changed:
- Adds `TrueShuffleHookInstaller`, which first checks the known `SPTFreeTierPlaylistTrackShuffler` class and then scans loaded shuffle-related classes for the same selectors.
- Avoids a hard Orion class hook so missing/renamed classes do not crash the app at startup.
- Retries for a short window after launch so lazily-loaded Spotify classes can be patched when they appear.
- Adds a Settings > Patching toggle and localization.

Verification:
- Patch generation completed from the current upstream `main` branch.
- The full Theos/iOS build could not be run in this GitHub Actions environment because the repository requires the local Theos toolchain and iOS SDK setup.
"""
    pr = request(
        "POST",
        f"/repos/{UPSTREAM}/pulls",
        {
            "title": "Add runtime-safe True Shuffle toggle",
            "head": f"{login}:{BRANCH}",
            "base": "main",
            "body": body,
            "maintainer_can_modify": True,
        },
        ok=(201,),
    )
    print(f"Opened PR: {pr['html_url']} at {head_sha}")
    return pr["html_url"]


def main() -> int:
    user = request("GET", "/user")
    login = user["login"]
    print(f"Authenticated as {login}")

    ensure_fork(login)

    upstream_ref = request("GET", f"/repos/{UPSTREAM}/git/ref/heads/main")
    base_sha = upstream_ref["object"]["sha"]
    base_commit = request("GET", f"/repos/{UPSTREAM}/git/commits/{base_sha}")
    base_tree = base_commit["tree"]["sha"]

    files = changed_files()
    tree = []
    for path, content in files.items():
        blob = request(
            "POST",
            f"/repos/{login}/{REPO}/git/blobs",
            {"content": content, "encoding": "utf-8"},
            ok=(201,),
        )
        tree.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    new_tree = request(
        "POST",
        f"/repos/{login}/{REPO}/git/trees",
        {"base_tree": base_tree, "tree": tree},
        ok=(201,),
    )
    commit = request(
        "POST",
        f"/repos/{login}/{REPO}/git/commits",
        {
            "message": "Add runtime-safe true shuffle toggle",
            "tree": new_tree["sha"],
            "parents": [base_sha],
        },
        ok=(201,),
    )

    branch_ref = request_or_none("GET", f"/repos/{login}/{REPO}/git/ref/heads/{BRANCH}")
    if branch_ref:
        request(
            "PATCH",
            f"/repos/{login}/{REPO}/git/refs/heads/{BRANCH}",
            {"sha": commit["sha"], "force": True},
        )
    else:
        request(
            "POST",
            f"/repos/{login}/{REPO}/git/refs",
            {"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]},
            ok=(201,),
        )

    pr_url = open_or_update_pr(login, commit["sha"])
    with open("true_shuffle_pr_report.md", "w", encoding="utf-8") as fh:
        fh.write(f"# True Shuffle PR report\n\n- Status: submitted\n- PR: {pr_url}\n- Commit: {commit['sha']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
