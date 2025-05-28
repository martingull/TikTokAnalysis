# Introduction
- A project to reverse engineer the tik-tok apk. The motivation for the project is to create a demo and some slideware to use as recruitment material. Chinese tech is having a hardtime in the west due to tiktok at the time this was created, so seemed like a good analysis to create some attention.
- Download a APK file from any APK repo. Then perform apk and androguard analysis.
- The idea of the project is to
    - Document current state: reverse engineer APK file and make report.
    - Create futute state: increase quality of apk decompiled file so resembels the original codebase more. I.e. making the code more readable to increase the signal of the input
    - Execution: Using LLM models better reconstruct the source code.

# Instructions
Easist thing is to run the `androguard.py` analysis and parse the output using a LLM model.
```bash
uv run androguard_analysis.py TikTok_39.2.1_APKPure.apk -o tik_tok_report.json
```
Copy paste the `tik_tok_report.json` into a LLM and start asking questins regarding privacy concerns.

# Cargo
- androguard_analysis.py - perform analysis of the APK file which can later be fed to a LLM model.
- apk_analysis.py - decompile the APK file so we can inspect the source code of the project.
- flatten_decompiled_files.py - TODO: make one large file from decompiled files to feed to context.
- reconstructed_sourcecode.py - TODO: based on hierarchy and flatten files create a reconstruction of the sourcecode.
- llm_analysis.py - TODO: go through the androguard and apk files using langchain, create analysis of results.
- dashboard.py - TODO: create a dashboard of the findings.
- requirements.txt - project ran fine on Python 3.12.9
