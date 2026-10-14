package com.staymart.controller;

import com.staymart.common.ApiResponse;
import com.staymart.service.FileStorageService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

@RestController
@RequestMapping("/api/files")
@Tag(name = "Files", description = "Image upload and serving")
public class FileController {

    private final FileStorageService fileStorageService;

    public FileController(FileStorageService fileStorageService) {
        this.fileStorageService = fileStorageService;
    }

    @PostMapping("/upload")
    @Operation(summary = "Upload an image, returns the public URL", security = @SecurityRequirement(name = "bearerAuth"))
    public ApiResponse<Map<String, String>> upload(@RequestParam("file") MultipartFile file) {
        String url = fileStorageService.store(file);
        return ApiResponse.ok(Map.of("url", url));
    }

    @GetMapping("/{filename}")
    @Operation(summary = "Serve an uploaded image")
    public ResponseEntity<Resource> download(@PathVariable String filename) {
        Resource resource = fileStorageService.load(filename);
        String contentType = fileStorageService.contentType(filename);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(contentType == null
                        ? MediaType.APPLICATION_OCTET_STREAM_VALUE : contentType))
                .header(HttpHeaders.CACHE_CONTROL, "public, max-age=86400")
                .body(resource);
    }
}