package org.example.seed;

import lombok.RequiredArgsConstructor;
import net.datafaker.Faker;
import org.example.entities.UserEntity;
import org.example.repositories.IUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class UserSeed implements CommandLineRunner {

    private final IUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (userRepository.existsByUsername("admin")) {
            return;
        }

        Faker faker = new Faker();

        UserEntity admin = new UserEntity();
        admin.setUsername("admin");
        admin.setEmail("admin@test.com");
        admin.setPassword(passwordEncoder.encode("admin12345"));
        userRepository.save(admin);

        int created = 0;
        while (created < 10) {
            String username = faker.name().username();
            if (userRepository.existsByUsername(username)) {
                continue;
            }

            UserEntity user = new UserEntity();
            user.setUsername(username);
            user.setEmail(faker.internet().emailAddress());
            user.setPassword(passwordEncoder.encode("user12345"));
            userRepository.save(user);
            created++;
        }
    }
}