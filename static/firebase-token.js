import { initializeApp } from
    "https://www.gstatic.com/firebasejs/10.13.2/firebase-app.js";

import { getMessaging, getToken } from
    "https://www.gstatic.com/firebasejs/10.13.2/firebase-messaging.js";


const firebaseConfig = {
    apiKey: "AIzaSyAiIajdSZtR3e9clD5MHRbFjMBThAO4bCc",
    authDomain: "bbau-student-parent-portal.firebaseapp.com",
    projectId: "bbau-student-parent-portal",
    storageBucket: "bbau-student-parent-portal.firebasestorage.app",
    messagingSenderId: "625608588923",
    appId: "1:625608588923:web:a5a23ffdca5d45cc25ecde"
};


const app = initializeApp(firebaseConfig);

const messaging = getMessaging(app);


async function getFCMToken() {

    try {

        const permission =
            await Notification.requestPermission();

        if (permission !== "granted") {

            console.log("Notification permission denied.");

            return null;
        }


        const token = await getToken(messaging, {

            vapidKey: "duzU5rjdHvBR4Tabbd-otf:APA91bHg0cWu6V6hh79ke3tfmMas4no_pin8tZ5QuPQsKWE-4sNxFAF7rrAAlHq-dr0eXs0H5jOh6eg0cDTHomV3bBVQZg6CzJyVqeeSjllJV_qYb6yVz9o"

        });


        if (token) {

            console.log("FCM TOKEN:", token);

            return token;

        } else {

            console.log("No FCM token available.");

            return null;
        }

    } catch (error) {

        console.error(
            "FCM token error:",
            error
        );

        return null;
    }
}


getFCMToken();