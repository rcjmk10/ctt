package com.delegate.service.email;

import com.delegate.model.OOOSetting;
import com.delegate.model.Delegation;
import com.google.api.services.gmail.Gmail;
import com.google.api.services.gmail.model.*;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.ArrayList;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Base64;

@Service
public class GmailService implements EmailProviderService {
    private static final Logger logger = LoggerFactory.getLogger(GmailService.class);
    private final Gmail gmailClient;

    public GmailService(Gmail gmailClient) {
        this.gmailClient = gmailClient;
    }

    @Override
    public void setOOOSetting(String userId, OOOSetting setting) {
        try {
            VacationSettings vacationSettings = new VacationSettings();
            vacationSettings.setEnableAutoReply(true);
            vacationSettings.setResponseSubject("Out of Office");
            vacationSettings.setResponseBodyPlainText(setting.getMessage());
            vacationSettings.setStartTime(setting.getStartDate().toEpochSecond() * 1000);
            vacationSettings.setEndTime(setting.getEndDate().toEpochSecond() * 1000);

            gmailClient.users().settings().updateVacation(userId, vacationSettings).execute();
        } catch (Exception e) {
            logger.error("Failed to set OOO setting in Gmail", e);
            throw new RuntimeException("Failed to set OOO setting in Gmail", e);
        }
    }

    @Override
    public void clearOOOSetting(String userId) {
        try {
            VacationSettings vacationSettings = new VacationSettings();
            vacationSettings.setEnableAutoReply(false);
            gmailClient.users().settings().updateVacation(userId, vacationSettings).execute();
        } catch (Exception e) {
            logger.error("Failed to clear OOO setting in Gmail", e);
            throw new RuntimeException("Failed to clear OOO setting in Gmail", e);
        }
    }

    @Override
    public OOOSetting getOOOSetting(String userId) {
        try {
            VacationSettings vacationSettings = gmailClient.users().settings().getVacation(userId).execute();
            
            if (!vacationSettings.getEnableAutoReply()) {
                return null;
            }

            OOOSetting setting = new OOOSetting();
            setting.setId("gmail-" + userId);
            setting.setUserId(userId);
            setting.setStartDate(OffsetDateTime.ofEpochSecond(vacationSettings.getStartTime() / 1000, 0, ZoneOffset.UTC));
            setting.setEndDate(OffsetDateTime.ofEpochSecond(vacationSettings.getEndTime() / 1000, 0, ZoneOffset.UTC));
            setting.setMessage(vacationSettings.getResponseBodyPlainText());
            setting.setStatus("active");
            setting.setCreatedAt(OffsetDateTime.now(ZoneOffset.UTC));
            setting.setUpdatedAt(OffsetDateTime.now(ZoneOffset.UTC));
            
            return setting;
        } catch (Exception e) {
            logger.error("Failed to get OOO setting from Gmail", e);
            throw new RuntimeException("Failed to get OOO setting from Gmail", e);
        }
    }

    @Override
    public void createDelegation(Delegation delegation) {
        try {
            // Gmail uses labels for delegation
            Label delegateLabel = new Label();
            delegateLabel.setName("Delegate: " + delegation.getDelegateId());
            delegateLabel.setLabelListVisibility("labelShow");
            delegateLabel.setMessageListVisibility("show");
            
            Label createdLabel = gmailClient.users().labels().create(delegation.getDelegatorId(), delegateLabel).execute();
            
            // Create a filter to forward emails to the delegate
            Filter filter = new Filter();
            filter.setAction(new FilterAction().setAddLabelIds(List.of(createdLabel.getId())));
            filter.setCriteria(new FilterCriteria().setFrom(delegation.getDelegateId()));
            
            gmailClient.users().settings().filters().create(delegation.getDelegatorId(), filter).execute();

            // If there's an active OOO setting, apply it
            OOOSetting oooSetting = getOOOSetting(delegation.getDelegatorId());
            if (oooSetting != null && "active".equals(oooSetting.getStatus())) {
                setOOOSetting(delegation.getDelegatorId(), oooSetting);
            }
        } catch (Exception e) {
            logger.error("Failed to create delegation in Gmail", e);
            throw new RuntimeException("Failed to create delegation in Gmail", e);
        }
    }

    @Override
    public void removeDelegation(Delegation delegation) {
        try {
            // Get all labels
            ListLabelsResponse labelsResponse = gmailClient.users().labels().list(delegation.getDelegatorId()).execute();
            
            // Find and delete the delegate label
            for (Label label : labelsResponse.getLabels()) {
                if (label.getName().startsWith("Delegate: " + delegation.getDelegateId())) {
                    gmailClient.users().labels().delete(delegation.getDelegatorId(), label.getId()).execute();
                    break;
                }
            }
            
            // Remove the filter
            ListFiltersResponse filtersResponse = gmailClient.users().settings().filters().list(delegation.getDelegatorId()).execute();
            for (Filter filter : filtersResponse.getFilter()) {
                if (filter.getCriteria().getFrom().equals(delegation.getDelegateId())) {
                    gmailClient.users().settings().filters().delete(delegation.getDelegatorId(), filter.getId()).execute();
                    break;
                }
            }
        } catch (Exception e) {
            logger.error("Failed to remove delegation in Gmail", e);
            throw new RuntimeException("Failed to remove delegation in Gmail", e);
        }
    }

    @Override
    public void updateDelegation(Delegation delegation) {
        try {
            // Gmail doesn't support updating delegation permissions directly
            // We need to remove and recreate the delegation
            removeDelegation(delegation);
            createDelegation(delegation);
        } catch (Exception e) {
            logger.error("Failed to update delegation in Gmail", e);
            throw new RuntimeException("Failed to update delegation in Gmail", e);
        }
    }

    @Override
    public List<Delegation> getDelegations(String userId) {
        try {
            List<Delegation> result = new ArrayList<>();
            
            // Get all labels
            ListLabelsResponse labelsResponse = gmailClient.users().labels().list(userId).execute();
            
            // Find delegate labels
            for (Label label : labelsResponse.getLabels()) {
                if (label.getName().startsWith("Delegate: ")) {
                    String delegateId = label.getName().substring("Delegate: ".length());
                    
                    Delegation delegation = new Delegation();
                    delegation.setId("gmail-" + userId + "-" + delegateId);
                    delegation.setDelegatorId(userId);
                    delegation.setDelegateId(delegateId);
                    delegation.setStartDate(OffsetDateTime.now(ZoneOffset.UTC));
                    delegation.setEndDate(OffsetDateTime.now(ZoneOffset.UTC).plusYears(1));
                    delegation.setStatus("active");
                    delegation.setPermissions(List.of("read", "write")); // Gmail has limited permission options
                    delegation.setCreatedAt(OffsetDateTime.now(ZoneOffset.UTC));
                    delegation.setUpdatedAt(OffsetDateTime.now(ZoneOffset.UTC));
                    
                    result.add(delegation);
                }
            }
            
            return result;
        } catch (Exception e) {
            logger.error("Failed to get delegations from Gmail", e);
            throw new RuntimeException("Failed to get delegations from Gmail", e);
        }
    }
} 