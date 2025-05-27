package com.delegate.controller;

import com.delegate.model.Delegation;
import com.delegate.service.DelegationService;
import com.delegate.util.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/delegations")
@RequiredArgsConstructor
public class DelegationController {
    private final DelegationService delegationService;

    @GetMapping("/me")
    public ResponseEntity<List<Delegation>> getMyDelegations() {
        UUID userId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(delegationService.findByUserId(userId));
    }

    @GetMapping("/me/active")
    public ResponseEntity<List<Delegation>> getMyActiveDelegations() {
        UUID userId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(delegationService.findActiveDelegations(userId, LocalDate.now()));
    }

    @GetMapping("/delegated-to-me")
    public ResponseEntity<List<Delegation>> getDelegationsToMe() {
        UUID userId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(delegationService.findByDelegateUserId(userId));
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @delegationService.findByUserId(#id).stream().anyMatch(d -> d.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<List<Delegation>> getUserDelegations(@PathVariable UUID id) {
        return ResponseEntity.ok(delegationService.findByUserId(id));
    }

    @PostMapping
    public ResponseEntity<Delegation> createDelegation(@RequestBody Delegation delegation) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(delegationService.createDelegation(delegation, actorId));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @delegationService.findByUserId(#id).stream().anyMatch(d -> d.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<Delegation> updateDelegation(
        @PathVariable UUID id,
        @RequestBody Delegation delegation
    ) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(delegationService.updateDelegation(id, delegation, actorId));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @delegationService.findByUserId(#id).stream().anyMatch(d -> d.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<Void> deleteDelegation(@PathVariable UUID id) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        delegationService.deleteDelegation(id, actorId);
        return ResponseEntity.ok().build();
    }
} 