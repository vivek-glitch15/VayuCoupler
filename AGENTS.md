# VayuCoupler Automation & Git Sync Guidelines

## Two-Way GitHub Synchronization Rule
1. **Always Pull Remote Updates First**:
   - Before executing any task or command, check for and pull remote updates:
     `git pull --rebase origin main`
   - If new commits were pushed to GitHub, integrate them immediately into the local `VayuCoupler` folder.

2. **Always Commit & Push Local Updates**:
   - Whenever code or assets are added, modified, or fixed in the `VayuCoupler` folder, automatically commit with a concise conventional commit message and push to GitHub:
     `git add -A && git commit -m "..." && git push origin main`
   - This ensures GitHub (`vivek-glitch15/VayuCoupler`), Vercel (`https://vayucoupler.vercel.app`), and Render remain 100% updated in real time.

3. **Parity Between Web App & Offline Windows/Mobile App**:
   - Ensure feature parity across `index.html`, `VayuCoupler_Windows_Offline_App.html`, and `backend/app/static/VayuCoupler_Standalone_Mobile_App.html`.
