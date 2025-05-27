package com.delegate.config;

import com.microsoft.graph.authentication.TokenCredentialAuthProvider;
import com.microsoft.graph.requests.GraphServiceClient;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.gmail.Gmail;
import com.google.api.services.gmail.GmailScopes;
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@Configuration
public class EmailProviderConfig {

    @Value("${azure.client-id}")
    private String azureClientId;

    @Value("${azure.client-secret}")
    private String azureClientSecret;

    @Value("${azure.tenant-id}")
    private String azureTenantId;

    @Value("${gmail.credentials-file}")
    private String gmailCredentialsFile;

    @Bean
    public GraphServiceClient graphClient() {
        List<String> scopes = Arrays.asList("https://graph.microsoft.com/.default");
        
        TokenCredentialAuthProvider authProvider = new TokenCredentialAuthProvider(
            scopes,
            new ClientSecretCredentialBuilder()
                .clientId(azureClientId)
                .clientSecret(azureClientSecret)
                .tenantId(azureTenantId)
                .build()
        );

        return GraphServiceClient.builder()
            .authenticationProvider(authProvider)
            .buildClient();
    }

    @Bean
    public Gmail gmailClient() throws IOException {
        GoogleCredentials credentials = GoogleCredentials.fromStream(
            getClass().getResourceAsStream(gmailCredentialsFile)
        ).createScoped(Arrays.asList(GmailScopes.GMAIL_SETTINGS_BASIC, GmailScopes.GMAIL_LABELS));

        return new Gmail.Builder(
            GoogleNetHttpTransport.newTrustedTransport(),
            JacksonFactory.getDefaultInstance(),
            new HttpCredentialsAdapter(credentials)
        )
        .setApplicationName("Delegate")
        .build();
    }
} 