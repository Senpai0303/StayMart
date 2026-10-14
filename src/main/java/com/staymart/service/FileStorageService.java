package com.staymart.service;

import com.staymart.exception.BadRequestException;
import com.staymart.exception.ResourceNotFoundException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;
import java.util.UUID;

@Service
public class FileStorageService {

    private static final Set<String> ALLOWED_EXTENSIONS =
            Set.of(".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg");

    private final Path uploadDir;
    private final String baseUrl;

    public FileStorageService(@Value("${app.upload.dir}") String directory,
                              @Value("${app.upload.base-url}") String baseUrl) {
        this.uploadDir = Paths.get(directory).toAbsolutePath().normalize();
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
        try {
            Files.createDirectories(uploadDir);
        } catch (IOException ex) {
            throw new IllegalStateException("Could not create upload directory: " + uploadDir, ex);
        }
    }

    public String store(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new BadRequestException("Please attach a file");
        }

        String originalName = StringUtils.cleanPath(
                file.getOriginalFilename() == null ? "file" : file.getOriginalFilename());
        String extension = "";
        int dotIndex = originalName.lastIndexOf('.');
        if (dotIndex > 0) {
            extension = originalName.substring(dotIndex).toLowerCase();
        }
        if (!ALLOWED_EXTENSIONS.contains(extension)) {
            throw new BadRequestException("Only image files are allowed: " + String.join(", ", ALLOWED_EXTENSIONS));
        }

        String filename = UUID.randomUUID() + extension;
        try {
            Files.copy(file.getInputStream(), uploadDir.resolve(filename));
        } catch (IOException ex) {
            throw new BadRequestException("Could not store file, please try again");
        }

        return baseUrl + "/api/files/" + filename;
    }

    public Resource load(String filename) {
        try {
            Path filePath = uploadDir.resolve(filename).normalize();
            if (!filePath.startsWith(uploadDir)) {
                throw new ResourceNotFoundException("File not found");
            }
            Resource resource = new UrlResource(filePath.toUri());
            if (!resource.exists() || !resource.isReadable()) {
                throw new ResourceNotFoundException("File not found: " + filename);
            }
            return resource;
        } catch (MalformedURLException ex) {
            throw new ResourceNotFoundException("File not found: " + filename);
        }
    }

    public String contentType(String filename) {
        try {
            return Files.probeContentType(uploadDir.resolve(filename).normalize());
        } catch (IOException ex) {
            return "application/octet-stream";
        }
    }
}