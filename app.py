from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Check if ID is registered for event
def verify_attendee(attendee_id, attendee_df):
    if attendee_id in attendee_df["ID"].to_list():
        return True
    else:
        return False

# Receive attendee ID from phone and verify
@app.route("/verify", methods=["GET"])
def verify():
    attendee_df = pd.read_excel("output.xlsx")
    attendee_id = request.args.get("id")
    if verify_attendee(attendee_id, attendee_df):
        attendee = attendee_df.loc[attendee_df["ID"] == attendee_id].iloc[0]
        attendee_df["SHOW"][attendee_df["ID"] == attendee_id] = "YES"
        return render_template(
            "welcome.html",
            first_name=attendee["FIRST NAME"],
            last_name=attendee["LAST NAME"],
            company=attendee["COMPANY"],
        )
        
    else:
        return render_template("not_registered.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
