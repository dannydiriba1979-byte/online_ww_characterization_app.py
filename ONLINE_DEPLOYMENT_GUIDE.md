# AquaEstimate — Online deployment guide

This is a Streamlit web application for estimating wastewater influent BOD5, TN and TP from routine COD and TSS inputs. Each target has a dedicated output panel. COD is the only input required for BOD5; COD and TSS are required for TN and TP.

## Files required

- `app.py` — web interface and prediction logic
- `influent_model_bundle.joblib` — trained estimators
- `requirements.txt` — Python dependencies

## Deploy on Streamlit Community Cloud

1. Download and extract the ZIP archive.
2. Create a GitHub repository and upload the three required files above to the repository root.
3. Visit https://share.streamlit.io/ and sign in.
4. Choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
5. Deploy. Once Streamlit finishes building, it will provide a hosted URL.

A public URL cannot be created from this package alone; deployment requires the user's hosting account and repository authorization.

## Run in Google Colab (interactive preview)

Upload `app.py`, `influent_model_bundle.joblib`, and `requirements.txt` to a Colab runtime. Install dependencies with `!pip install -r requirements.txt`. Streamlit is a server-based app, so running the script in a notebook cell alone will not create a public website; use Streamlit Community Cloud for the stable online deployment.

## Limitations

The app uses the supplied trained models. BOD5 is a candidate requiring prospective validation. TN and TP estimates are research-only due to limited holdout data and poor held-out R². Do not replace laboratory testing based solely on these predictions.
