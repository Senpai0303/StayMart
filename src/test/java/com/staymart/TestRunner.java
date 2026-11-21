package com.staymart;

import com.staymart.entity.EntityModelTest;
import com.staymart.security.JwtAuthenticationFilterTest;
import com.staymart.service.RecommendationServiceTest;
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;

import java.io.PrintWriter;

import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;

public class TestRunner {
    public static void main(String[] args) {
        LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
                .selectors(
                        selectClass(RecommendationServiceTest.class),
                        selectClass(JwtAuthenticationFilterTest.class),
                        selectClass(EntityModelTest.class)
                )
                .build();

        Launcher launcher = LauncherFactory.create();
        SummaryGeneratingListener listener = new SummaryGeneratingListener();
        launcher.registerTestExecutionListeners(listener);

        launcher.execute(request);

        TestExecutionSummary summary = listener.getSummary();
        summary.printTo(new PrintWriter(System.out));

        if (summary.getTotalFailureCount() > 0) {
            System.err.println("=== FAILURE DETAILS ===");
            for (TestExecutionSummary.Failure failure : summary.getFailures()) {
                System.err.println("FAILED: " + failure.getTestIdentifier().getDisplayName());
                if (failure.getException() != null) {
                    failure.getException().printStackTrace(System.err);
                }
            }
            System.exit(1);
        } else {
            System.out.println("ALL TESTS PASSED SUCCESSFULLY!");
            System.exit(0);
        }
    }
}
