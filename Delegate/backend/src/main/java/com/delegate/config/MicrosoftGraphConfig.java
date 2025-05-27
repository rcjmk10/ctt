package com.delegate.config;

import com.microsoft.graph.authentication.TokenCredentialAuthProvider;
import com.microsoft.graph.requests.GraphServiceClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.Arrays;

@Configuration
public class MicrosoftGraphConfig {
    @Value("${microsoft.graph.client-id}")
    private String clientId;

    @Value("${microsoft.graph.client-secret}")
    private String clientSecret;

    @Value("${microsoft.graph.tenant-id}")
    private String tenantId;

    @Bean
    public GraphServiceClient graphClient() {
        TokenCredentialAuthProvider authProvider = new TokenCredentialAuthProvider(
            Arrays.asList("https://graph.microsoft.com/.default"),
            clientId,
            clientSecret,
            tenantId
        );

        return GraphServiceClient.builder()
            .authenticationProvider(authProvider)
            .buildClient();
    }
} 