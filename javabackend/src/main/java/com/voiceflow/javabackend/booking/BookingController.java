package com.voiceflow.javabackend.booking;

import com.voiceflow.javabackend.common.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/bookings")
@RequiredArgsConstructor
public class BookingController {

    private final BookingRepository bookingRepository;

    @PostMapping
    public ResponseEntity<Booking> createBooking(@RequestBody Booking booking) {
        if (booking.getStatus() == null) {
            booking.setStatus(BookingStatus.CONFIRMED);
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(bookingRepository.save(booking));
    }

    @GetMapping
    public ResponseEntity<List<Booking>> getBookings(@RequestParam(required = false) UUID companyId) {
        List<Booking> list = companyId != null
                ? bookingRepository.findByCompanyId(companyId)
                : bookingRepository.findAll();
        return ResponseEntity.ok(list);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Booking> getBookingById(@PathVariable UUID id) {
        return ResponseEntity.ok(bookingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Booking", id)));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<Booking> updateBookingStatus(
            @PathVariable UUID id,
            @RequestBody Map<String, String> body
    ) {
        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Booking", id));
        if (body.containsKey("status")) {
            booking.setStatus(BookingStatus.valueOf(body.get("status").toUpperCase()));
        }
        return ResponseEntity.ok(bookingRepository.save(booking));
    }
}
