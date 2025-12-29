package org.example.callgate;

import android.telecom.Call;
import android.telecom.CallScreeningService;
import android.content.SharedPreferences;
import java.util.Set;

public class CallBlockerService extends CallScreeningService {

    @Override
    public void onScreenCall(Call.Details details) {

        String incoming =
            details.getHandle().getSchemeSpecificPart();

        SharedPreferences prefs =
            getSharedPreferences("allowed_calls", MODE_PRIVATE);

        Set<String> allowed =
            prefs.getStringSet("numbers", null);

        CallResponse.Builder response =
            new CallResponse.Builder();

        if (allowed != null && allowed.contains(incoming)) {
            response.setDisallowCall(false);
        } else {
            response.setRejectCall(true)
                    .setSkipCallLog(true)
                    .setSkipNotification(true);
        }

        respondToCall(details, response.build());
    }
}
