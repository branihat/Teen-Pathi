class AppConstants {
  // API Configuration
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String apiVersion = 'v1';
  
  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const String themeKey = 'theme_mode';
  static const String languageKey = 'language';
  
  // App Configuration
  static const String appName = 'Betting App';
  static const String appVersion = '1.0.0';
  static const Duration apiTimeout = Duration(seconds: 30);
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Betting Configuration
  static const double minBetAmount = 1.0;
  static const double maxBetAmount = 10000.0;
  static const double defaultBetAmount = 10.0;
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // Cache Configuration
  static const Duration cacheExpiry = Duration(hours: 1);
  static const Duration longCacheExpiry = Duration(days: 7);
  
  // Firebase Configuration
  static const String fcmTopic = 'betting_notifications';
  
  // Payment Configuration
  static const String stripePublishableKey = 'pk_test_your_stripe_key';
  static const List<String> supportedCurrencies = ['USD', 'EUR', 'GBP'];
  static const String defaultCurrency = 'USD';
  
  // Game Types
  static const List<String> gameTypes = [
    'lottery',
    'casino',
    'sports',
    'poker'
  ];
  
  // Notification Types
  static const List<String> notificationTypes = [
    'game_update',
    'promotion',
    'bet_result',
    'deposit_confirmation',
    'withdrawal_confirmation',
    'account_update',
    'general'
  ];
  
  // Error Messages
  static const String networkError = 'Network error occurred';
  static const String unauthorizedError = 'Unauthorized access';
  static const String serverError = 'Server error occurred';
  static const String unknownError = 'An unknown error occurred';
  
  // Success Messages
  static const String loginSuccess = 'Login successful';
  static const String registrationSuccess = 'Registration successful';
  static const String betPlacedSuccess = 'Bet placed successfully';
  static const String profileUpdateSuccess = 'Profile updated successfully';
}

enum UserRole {
  user,
  admin,
  superAdmin,
}

enum UserStatus {
  active,
  inactive,
  suspended,
}

enum GameStatus {
  active,
  inactive,
  maintenance,
}

enum GameType {
  lottery,
  casino,
  sports,
  poker,
}

enum BetStatus {
  pending,
  won,
  lost,
  cancelled,
  refunded,
}

enum TransactionType {
  deposit,
  withdrawal,
  betPlaced,
  betWon,
  betRefund,
  bonus,
  commission,
}
