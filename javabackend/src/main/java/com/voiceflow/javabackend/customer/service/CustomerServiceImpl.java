package com.voiceflow.javabackend.customer.service;

import com.voiceflow.javabackend.common.exception.ResourceNotFoundException;
import com.voiceflow.javabackend.customer.dto.CustomerCreateRequest;
import com.voiceflow.javabackend.customer.dto.CustomerResponse;
import com.voiceflow.javabackend.customer.entity.Customer;
import com.voiceflow.javabackend.customer.repository.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class CustomerServiceImpl implements CustomerService {

    private final CustomerRepository customerRepository;

    @Override
    public CustomerResponse createCustomer(CustomerCreateRequest request) {
        Customer customer = Customer.builder()
                .companyId(request.companyId())
                .name(request.name())
                .email(request.email())
                .phone(request.phone())
                .build();
        return toResponse(customerRepository.save(customer));
    }

    @Override
    public CustomerResponse getCustomerById(UUID id) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Customer", id));
        return toResponse(customer);
    }

    @Override
    public List<CustomerResponse> getCustomers(UUID companyId) {
        List<Customer> list = companyId != null
                ? customerRepository.findByCompanyId(companyId)
                : customerRepository.findAll();
        return list.stream().map(this::toResponse).toList();
    }

    @Override
    public void deleteCustomer(UUID id) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Customer", id));
        customerRepository.delete(customer);
    }

    private CustomerResponse toResponse(Customer c) {
        return new CustomerResponse(
                c.getId(),
                c.getCompanyId(),
                c.getName(),
                c.getEmail(),
                c.getPhone(),
                c.getCreatedAt(),
                c.getUpdatedAt()
        );
    }
}
