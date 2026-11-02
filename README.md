# Mariam's Reaction Lab (Android)

A full-screen WebView app that runs the 3D chemistry lab offline from
`app/src/main/assets/index.html`. No extra libraries: just the Android SDK.

- Package: `org.radon.reactionlab` · minSdk 26 (Android 8.0) · targetSdk 34
- Saves missions and discoveries in the WebView's local storage
- Internet is only used for the web fonts; without it the app uses system fonts

## Build the APK in Android Studio
1. **File → Open** and choose this `MariamsReactionLab` folder. Let Gradle sync.
2. **Build → Build App Bundle(s) / APK(s) → Build APK(s)**.
3. Click **locate** in the pop-up. The file is `app/build/outputs/apk/debug/app-debug.apk`.
4. Copy it to the phone and open it (allow "Install unknown apps" for your file manager once).

Or press ▶ Run with the phone plugged in (USB debugging on) to install it directly.

## Build the APK on GitHub (no Android Studio needed)
1. Create a new private repository and push this folder to it.
2. Open the **Actions** tab. The **Build APK** workflow runs automatically.
3. When it finishes, download **Mariams-Reaction-Lab-apk** from the run's *Artifacts*.

The release build is signed with the debug key so it installs straight away.
Before publishing on Google Play, create your own keystore
(**Build → Generate Signed Bundle / APK**) and use that instead.

## Updating the lab
Replace `app/src/main/assets/index.html` with the new offline HTML file,
raise `versionCode` in `app/build.gradle`, and build again.
