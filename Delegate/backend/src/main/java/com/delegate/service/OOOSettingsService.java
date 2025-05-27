package com.delegate.service;

import com.delegate.model.OOOSetting;
import com.delegate.repository.OOOSettingRepository;
import com.delegate.service.email.EmailProviderFactory;
import com.delegate.service.email.EmailProviderService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.Optional;

@Service
public class OOOSettingsService {
    private static final Logger logger = LoggerFactory.getLogger(OOOSettingsService.class);
    
    private final OOOSettingRepository oooSettingRepository;
    private final EmailProviderFactory emailProviderFactory;

    public OOOSettingsService(OOOSettingRepository oooSettingRepository, EmailProviderFactory emailProviderFactory) {
        this.oooSettingRepository = oooSettingRepository;
        this.emailProviderFactory = emailProviderFactory;
    }

    @Transactional
    public OOOSetting createOOOSetting(OOOSetting setting, String providerType) {
        try {
            // Save to database
            OOOSetting savedSetting = oooSettingRepository.save(setting);
            
            // Get the appropriate email provider
            EmailProviderService provider = emailProviderFactory.getProvider(providerType);
            
            // Set OOO in the email provider
            provider.setOOOSetting(savedSetting.getUserId(), savedSetting);
            
            return savedSetting;
        } catch (Exception e) {
            logger.error("Failed to create OOO setting", e);
            throw new RuntimeException("Failed to create OOO setting", e);
        }
    }

    @Transactional
    public void clearOOOSetting(String userId, String providerType) {
        try {
            // Clear in email provider
            EmailProviderService provider = emailProviderFactory.getProvider(providerType);
            provider.clearOOOSetting(userId);
            
            // Clear in database
            oooSettingRepository.deleteByUserId(userId);
        } catch (Exception e) {
            logger.error("Failed to clear OOO setting", e);
            throw new RuntimeException("Failed to clear OOO setting", e);
        }
    }

    @Transactional
    public OOOSetting updateOOOSetting(String id, OOOSetting updatedSetting, String providerType) {
        try {
            Optional<OOOSetting> existingSettingOpt = oooSettingRepository.findById(id);
            if (existingSettingOpt.isPresent()) {
                OOOSetting existingSetting = existingSettingOpt.get();
                
                // Update fields
                existingSetting.setStartDate(updatedSetting.getStartDate());
                existingSetting.setEndDate(updatedSetting.getEndDate());
                existingSetting.setMessage(updatedSetting.getMessage());
                existingSetting.setStatus(updatedSetting.getStatus());
                
                // Save to database
                OOOSetting savedSetting = oooSettingRepository.save(existingSetting);
                
                // Update in email provider
                EmailProviderService provider = emailProviderFactory.getProvider(providerType);
                provider.setOOOSetting(savedSetting.getUserId(), savedSetting);
                
                return savedSetting;
            }
            throw new RuntimeException("OOO setting not found with id: " + id);
        } catch (Exception e) {
            logger.error("Failed to update OOO setting", e);
            throw new RuntimeException("Failed to update OOO setting", e);
        }
    }

    public OOOSetting getOOOSetting(String userId, String providerType) {
        try {
            // Get from email provider
            EmailProviderService provider = emailProviderFactory.getProvider(providerType);
            OOOSetting providerSetting = provider.getOOOSetting(userId);
            
            // Get from database
            Optional<OOOSetting> dbSettingOpt = oooSettingRepository.findByUserId(userId);
            
            // Merge and return
            return mergeOOOSettings(providerSetting, dbSettingOpt.orElse(null));
        } catch (Exception e) {
            logger.error("Failed to get OOO setting", e);
            throw new RuntimeException("Failed to get OOO setting", e);
        }
    }

    private OOOSetting mergeOOOSettings(OOOSetting providerSetting, OOOSetting dbSetting) {
        // If we have a provider setting, use that
        if (providerSetting != null) {
            return providerSetting;
        }
        
        // Otherwise, use the database setting
        return dbSetting;
    }
} 