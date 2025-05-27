package com.delegate.service.email;

import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.Map;
import java.util.HashMap;

@Component
public class EmailProviderFactory {
    private final Map<String, EmailProviderService> providers;

    @Autowired
    public EmailProviderFactory(Outlook365Service outlook365Service, GmailService gmailService) {
        providers = new HashMap<>();
        providers.put("outlook365", outlook365Service);
        providers.put("gmail", gmailService);
    }

    public EmailProviderService getProvider(String providerType) {
        EmailProviderService provider = providers.get(providerType.toLowerCase());
        if (provider == null) {
            throw new IllegalArgumentException("Unsupported email provider: " + providerType);
        }
        return provider;
    }
} 