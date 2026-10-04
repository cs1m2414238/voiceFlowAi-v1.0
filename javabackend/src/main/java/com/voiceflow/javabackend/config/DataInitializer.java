package com.voiceflow.javabackend.config;

import com.voiceflow.javabackend.company.entity.Company;
import com.voiceflow.javabackend.company.enums.IndustryType;
import com.voiceflow.javabackend.company.repository.CompanyRepository;
import com.voiceflow.javabackend.customer.entity.Customer;
import com.voiceflow.javabackend.customer.repository.CustomerRepository;
import com.voiceflow.javabackend.order.Order;
import com.voiceflow.javabackend.order.OrderRepository;
import com.voiceflow.javabackend.user.entity.User;
import com.voiceflow.javabackend.user.enums.UserRole;
import com.voiceflow.javabackend.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final CompanyRepository companyRepository;
    private final UserRepository userRepository;
    private final CustomerRepository customerRepository;
    private final OrderRepository orderRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (companyRepository.count() > 0) {
            return;
        }

        Company demoCompany = companyRepository.save(Company.builder()
                .name("VoiceFlow E-Commerce")
                .industryType(IndustryType.ECOMMERCE)
                .supportEmail("support@voiceflow.ai")
                .supportPhone("+1-800-555-0199")
                .active(true)
                .build());

        if (!userRepository.existsByEmail("admin@voiceflow.ai")) {
            userRepository.save(User.builder()
                    .userName("Admin User")
                    .email("admin@voiceflow.ai")
                    .passwordHash(passwordEncoder.encode("password123"))
                    .role(UserRole.COMPANY_ADMIN)
                    .company(demoCompany)
                    .active(true)
                    .build());
        }

        Customer demoCustomer = customerRepository.save(Customer.builder()
                .companyId(demoCompany.getId())
                .name("Alex Rivera")
                .email("alex@example.com")
                .phone("+1-555-0142")
                .build());

        orderRepository.saveAll(List.of(
                Order.builder()
                        .orderNumber("1001")
                        .companyId(demoCompany.getId())
                        .customerId(demoCustomer.getId())
                        .item("Wireless headphones")
                        .status("Shipped")
                        .expectedDate("5 Oct")
                        .build(),
                Order.builder()
                        .orderNumber("1002")
                        .companyId(demoCompany.getId())
                        .customerId(demoCustomer.getId())
                        .item("Running shoes")
                        .status("Processing")
                        .expectedDate("8 Oct")
                        .build(),
                Order.builder()
                        .orderNumber("1003")
                        .companyId(demoCompany.getId())
                        .customerId(demoCustomer.getId())
                        .item("Water bottle")
                        .status("Delivered")
                        .expectedDate("1 Oct")
                        .build()
        ));

        log.info("Seeded default VoiceFlow company ({}) and demo data.", demoCompany.getId());
    }
}
