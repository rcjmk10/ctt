package com.delegate.controller;

import com.delegate.model.OOOSetting;
import com.delegate.service.OOOSettingService;
import com.delegate.util.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/ooo-settings")
@RequiredArgsConstructor
public class OOOSettingController {
    private final OOOSettingService oooSettingService;

    @GetMapping("/me")
    public ResponseEntity<List<OOOSetting>> getMySettings() {
        UUID userId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(oooSettingService.findByUserId(userId));
    }

    @GetMapping("/me/active")
    public ResponseEntity<List<OOOSetting>> getMyActiveSettings() {
        UUID userId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(oooSettingService.findActiveSettings(userId, LocalDate.now()));
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @oooSettingService.findByUserId(#id).stream().anyMatch(s -> s.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<List<OOOSetting>> getUserSettings(@PathVariable UUID id) {
        return ResponseEntity.ok(oooSettingService.findByUserId(id));
    }

    @PostMapping
    public ResponseEntity<OOOSetting> createSetting(@RequestBody OOOSetting setting) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(oooSettingService.createSetting(setting, actorId));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @oooSettingService.findByUserId(#id).stream().anyMatch(s -> s.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<OOOSetting> updateSetting(
        @PathVariable UUID id,
        @RequestBody OOOSetting setting
    ) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        return ResponseEntity.ok(oooSettingService.updateSetting(id, setting, actorId));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or @oooSettingService.findByUserId(#id).stream().anyMatch(s -> s.getUser().getEmail().equals(authentication.name))")
    public ResponseEntity<Void> deleteSetting(@PathVariable UUID id) {
        UUID actorId = SecurityUtils.getCurrentUserId();
        oooSettingService.deleteSetting(id, actorId);
        return ResponseEntity.ok().build();
    }
} 