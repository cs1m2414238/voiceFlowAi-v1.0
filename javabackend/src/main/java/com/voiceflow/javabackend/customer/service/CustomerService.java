package com.voiceflow.javabackend.customer.service;

import com.voiceflow.javabackend.customer.dto.CustomerCreateRequest;
import com.voiceflow.javabackend.customer.dto.CustomerResponse;

import java.util.List;
import java.util.UUID;

public interface CustomerService {
    CustomerResponse createCustomer(CustomerCreateRequest request);
    CustomerResponse getCustomerById(UUID id);
    List<CustomerResponse> getCustomers(UUID companyId);
    void deleteCustomer(UUID id);
}
