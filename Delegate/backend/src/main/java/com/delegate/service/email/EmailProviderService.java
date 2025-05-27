package com.delegate.service.email;

import com.delegate.model.OOOSetting;
import com.delegate.model.Delegation;
import java.util.List;

public interface EmailProviderService {
    // OOO Settings
    void setOOOSetting(String userId, OOOSetting setting);
    void clearOOOSetting(String userId);
    OOOSetting getOOOSetting(String userId);

    // Delegation
    void createDelegation(Delegation delegation);
    void removeDelegation(Delegation delegation);
    void updateDelegation(Delegation delegation);
    List<Delegation> getDelegations(String userId);
} 