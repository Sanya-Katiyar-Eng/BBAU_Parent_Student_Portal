importScripts("https://www.gstatic.com/firebasejs/10.13.2/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.13.2/firebase-messaging-compat.js");

const firebaseConfig = {
    apiKey: "AIzaSyAiIajdSZtR3e9clD5MHRbFjMBThAO4bCc",
    authDomain: "bbau-student-parent-portal.firebaseapp.com",
    projectId: "bbau-student-parent-portal",
    storageBucket: "bbau-student-parent-portal.firebasestorage.app",
    messagingSenderId: "625608588923",
    appId: "1:625608588923:web:a5a23ffdca5d45cc25ecde"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {

    console.log("Background message received:", payload);

    const notificationTitle =
        payload.notification?.title ||
        "BBAU Attendance";

    const notificationOptions = {
        body:
            payload.notification?.body ||
            "You have a new attendance notification.",

        icon: "/favicon.png"
    };

    self.registration.showNotification(
        notificationTitle,
        notificationOptions
    );
});