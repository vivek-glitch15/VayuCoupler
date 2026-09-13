package in.gov.moes.vayucoupler;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.NetworkInfo;
import android.net.NetworkRequest;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends AppCompatActivity {

    // Live Production Frontend on Vercel (Proxied to Render Backend)
    public static final String TARGET_URL = "https://vayucoupler.vercel.app";
    public static final String OFFLINE_URL = "file:///android_asset/offline.html";
    private static final int LOCATION_PERMISSION_REQUEST = 1001;

    private WebView webView;
    private SwipeRefreshLayout swipeRefresh;
    private ProgressBar progressBar;
    private LinearLayout offlineLayout;
    private Button retryBtn;
    private GeolocationPermissions.Callback geoCallback;
    private String geoOrigin;
    private boolean isOfflineFallbackActive = false;
    private ConnectivityManager.NetworkCallback networkCallback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webView);
        swipeRefresh = findViewById(R.id.swipeRefresh);
        progressBar = findViewById(R.id.progressBar);
        offlineLayout = findViewById(R.id.offlineLayout);
        retryBtn = findViewById(R.id.retryBtn);

        // Configure Swipe to Refresh
        swipeRefresh.setColorSchemeColors(ContextCompat.getColor(this, R.color.accent_cyan));
        swipeRefresh.setProgressBackgroundColorSchemeColor(ContextCompat.getColor(this, R.color.header_dark));
        swipeRefresh.setOnRefreshListener(() -> {
            if (isNetworkAvailable()) {
                isOfflineFallbackActive = false;
                offlineLayout.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
                webView.loadUrl(TARGET_URL);
            } else {
                swipeRefresh.setRefreshing(false);
                loadOfflineApp();
            }
        });

        retryBtn.setOnClickListener(v -> {
            if (isNetworkAvailable()) {
                isOfflineFallbackActive = false;
                offlineLayout.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
                webView.loadUrl(TARGET_URL);
            } else {
                loadOfflineApp();
            }
        });

        configureWebView();

        if (isNetworkAvailable()) {
            loadOnlineApp();
        } else {
            loadOfflineApp();
        }

        registerNetworkMonitor();
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setGeolocationEnabled(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);

        // Allow local assets and offline storage
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);

        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // Custom User Agent suffix for app analytics
        String defaultUa = settings.getUserAgentString();
        settings.setUserAgentString(defaultUa + " VayuCoupler-Android-Hybrid/2.0");

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                    swipeRefresh.setRefreshing(false);
                }
            }

            @Override
            public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                geoCallback = callback;
                geoOrigin = origin;
                if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION)
                        != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(MainActivity.this,
                            new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                            LOCATION_PERMISSION_REQUEST);
                } else {
                    callback.invoke(origin, true, false);
                }
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.startsWith("https://vayucoupler.vercel.app") || 
                    url.contains("onrender.com") || 
                    url.startsWith("file:///android_asset/")) {
                    return false; // Keep inside webview
                }
                // Open external links in default browser
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(intent);
                return true;
            }

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                offlineLayout.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    // Fall back gracefully to the embedded 100% offline standalone engine
                    if (!isOfflineFallbackActive) {
                        runOnUiThread(() -> loadOfflineApp());
                    }
                }
            }
        });
    }

    private void loadOnlineApp() {
        isOfflineFallbackActive = false;
        offlineLayout.setVisibility(View.GONE);
        webView.setVisibility(View.VISIBLE);
        webView.loadUrl(TARGET_URL);
    }

    private void loadOfflineApp() {
        isOfflineFallbackActive = true;
        offlineLayout.setVisibility(View.GONE);
        webView.setVisibility(View.VISIBLE);
        swipeRefresh.setRefreshing(false);
        progressBar.setVisibility(View.GONE);
        webView.loadUrl(OFFLINE_URL);
    }

    private void registerNetworkMonitor() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm != null) {
                networkCallback = new ConnectivityManager.NetworkCallback() {
                    @Override
                    public void onAvailable(@NonNull Network network) {
                        runOnUiThread(() -> {
                            if (isOfflineFallbackActive) {
                                Toast.makeText(MainActivity.this, "🟢 Network restored! Syncing live CPCB/MoES telemetry...", Toast.LENGTH_SHORT).show();
                                loadOnlineApp();
                            }
                        });
                    }

                    @Override
                    public void onLost(@NonNull Network network) {
                        runOnUiThread(() -> {
                            if (!isOfflineFallbackActive) {
                                Toast.makeText(MainActivity.this, "📡 Offline Mode Activated — Running autonomous local model.", Toast.LENGTH_SHORT).show();
                                loadOfflineApp();
                            }
                        });
                    }
                };
                cm.registerDefaultNetworkCallback(networkCallback);
            }
        }
    }

    private boolean isNetworkAvailable() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        if (cm != null) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                Network network = cm.getActiveNetwork();
                if (network != null) {
                    NetworkCapabilities caps = cm.getNetworkCapabilities(network);
                    return caps != null && (caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
                                            caps.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
                                            caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET));
                }
            } else {
                NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                return activeNetwork != null && activeNetwork.isConnectedOrConnecting();
            }
        }
        return false;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == LOCATION_PERMISSION_REQUEST && geoCallback != null) {
            boolean allow = grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED;
            geoCallback.invoke(geoOrigin, allow, false);
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (networkCallback != null && Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm != null) {
                try {
                    cm.unregisterNetworkCallback(networkCallback);
                } catch (Exception ignored) {}
            }
        }
    }
}
