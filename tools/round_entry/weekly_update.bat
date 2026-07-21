@echo off
REM weekly_update.bat - the owner's one-command weekly updater (native Windows).
REM
REM A thin wrapper over the Python CLI (tools\round_entry\round_entry.py). It sets a portable,
REM deterministic environment and forwards every argument to the CLI. NO Python editing needed.
REM
REM THE 2-MINUTE WORKFLOW
REM   weekly_update.bat enter   --round 15 --body-file round15.csv
REM   weekly_update.bat confirm --round 15
REM   weekly_update.bat show    --round 15
REM   weekly_update.bat apply   --round 15
REM   weekly_update.bat recover
REM
REM APPLY IS GATED OFF BY DEFAULT (this build applies no real round). `apply` REFUSES and prints
REM instructions unless you arm BOTH halves LOCALLY for the run - no code edit, just two env vars:
REM   set INGEST_SCORE_APPLY_ARMED=1
REM   set INGEST_SCORE_APPLY=your-own-token
REM   weekly_update.bat apply --round 15
REM See tools\round_entry\README.md. Nothing is armed in the committed repo.
setlocal
set "HERE=%~dp0"
pushd "%HERE%\..\.." >nul
set "REPO=%CD%"

if not defined PYTHONHASHSEED set "PYTHONHASHSEED=0"
if not defined OPENBLAS_NUM_THREADS set "OPENBLAS_NUM_THREADS=1"
if not defined OMP_NUM_THREADS set "OMP_NUM_THREADS=1"
if not defined MKL_NUM_THREADS set "MKL_NUM_THREADS=1"
if not defined NUMEXPR_NUM_THREADS set "NUMEXPR_NUM_THREADS=1"

if not defined RL_VENDOR set "RL_VENDOR=%REPO%\vendor"
set "PYTHONPATH=%REPO%\engine\rl_after;%RL_VENDOR%;%PYTHONPATH%"

if not defined PYTHON set "PYTHON=python"
"%PYTHON%" "%REPO%\tools\round_entry\round_entry.py" %*
set "RC=%ERRORLEVEL%"
popd >nul
exit /b %RC%
