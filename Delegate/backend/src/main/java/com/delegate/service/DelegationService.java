package com.delegate.service;

import com.delegate.model.Delegation;
import com.delegate.repository.DelegationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class DelegationService {
    private final DelegationRepository delegationRepository;
    private final AuditLogService auditLogService;

    @Transactional(readOnly = true)
    public List<Delegation> findByUserId(UUID userId) {
        return delegationRepository.findByUserId(userId);
    }

    @Transactional(readOnly = true)
    public List<Delegation> findByDelegateUserId(UUID delegateUserId) {
        return delegationRepository.findByDelegateUserId(delegateUserId);
    }

    @Transactional(readOnly = true)
    public List<Delegation> findActiveDelegations(UUID userId, LocalDate date) {
        return delegationRepository.findByUserIdAndStartDateLessThanEqualAndEndDateGreaterThanEqual(
            userId, date, date);
    }

    @Transactional
    public Delegation createDelegation(Delegation delegation, UUID actorId) {
        validateDelegation(delegation);
        Delegation savedDelegation = delegationRepository.save(delegation);
        auditLogService.logCreation("Delegation", savedDelegation.getId(), actorId, savedDelegation);
        return savedDelegation;
    }

    @Transactional
    public Delegation updateDelegation(UUID id, Delegation delegationDetails, UUID actorId) {
        Delegation delegation = delegationRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Delegation not found"));
        
        validateDelegation(delegationDetails);
        
        Delegation oldDelegation = new Delegation();
        oldDelegation.setStartDate(delegation.getStartDate());
        oldDelegation.setEndDate(delegation.getEndDate());
        oldDelegation.setTaskType(delegation.getTaskType());
        oldDelegation.setDelegateUser(delegation.getDelegateUser());
        
        delegation.setStartDate(delegationDetails.getStartDate());
        delegation.setEndDate(delegationDetails.getEndDate());
        delegation.setTaskType(delegationDetails.getTaskType());
        delegation.setDelegateUser(delegationDetails.getDelegateUser());
        
        Delegation updatedDelegation = delegationRepository.save(delegation);
        auditLogService.logUpdate("Delegation", id, actorId, oldDelegation, updatedDelegation);
        return updatedDelegation;
    }

    @Transactional
    public void deleteDelegation(UUID id, UUID actorId) {
        Delegation delegation = delegationRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Delegation not found"));
        
        delegationRepository.deleteById(id);
        auditLogService.logDeletion("Delegation", id, actorId, delegation);
    }

    private void validateDelegation(Delegation delegation) {
        if (delegation.getStartDate().isAfter(delegation.getEndDate())) {
            throw new IllegalArgumentException("Start date must be before end date");
        }
        
        // Check for circular delegation
        if (delegation.getUser().getId().equals(delegation.getDelegateUser().getId())) {
            throw new IllegalArgumentException("Cannot delegate to yourself");
        }
        
        // Check for existing delegation conflicts
        List<Delegation> existingDelegations = delegationRepository
            .findByUserIdAndApplicationIdAndTaskType(
                delegation.getUser().getId(),
                delegation.getApplication().getId(),
                delegation.getTaskType()
            );
        
        for (Delegation existing : existingDelegations) {
            if (existing.getId().equals(delegation.getId())) {
                continue;
            }
            
            if (isDateRangeOverlapping(
                delegation.getStartDate(), delegation.getEndDate(),
                existing.getStartDate(), existing.getEndDate()
            )) {
                throw new IllegalArgumentException(
                    "Delegation conflict: Another delegation exists for the same task type and time period");
            }
        }
    }

    private boolean isDateRangeOverlapping(
        LocalDate start1, LocalDate end1,
        LocalDate start2, LocalDate end2
    ) {
        return !start1.isAfter(end2) && !start2.isAfter(end1);
    }
} 