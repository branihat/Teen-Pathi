import 'package:shared_preferences/shared_preferences.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'dart:convert';
import '../constants/app_constants.dart';

class StorageService {
  static final StorageService _instance = StorageService._internal();
  factory StorageService() => _instance;
  StorageService._internal();

  late SharedPreferences _prefs;
  late Box _secureBox;

  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    await Hive.initFlutter();
    _secureBox = await Hive.openBox('secure_storage');
  }

  // Token Management
  Future<void> setAccessToken(String token) async {
    await _secureBox.put(AppConstants.accessTokenKey, token);
  }

  Future<String?> getAccessToken() async {
    return _secureBox.get(AppConstants.accessTokenKey);
  }

  Future<void> setRefreshToken(String token) async {
    await _secureBox.put(AppConstants.refreshTokenKey, token);
  }

  Future<String?> getRefreshToken() async {
    return _secureBox.get(AppConstants.refreshTokenKey);
  }

  Future<void> clearAuthData() async {
    await _secureBox.delete(AppConstants.accessTokenKey);
    await _secureBox.delete(AppConstants.refreshTokenKey);
    await _secureBox.delete(AppConstants.userDataKey);
  }

  // User Data Management
  Future<void> setUserData(Map<String, dynamic> userData) async {
    await _secureBox.put(AppConstants.userDataKey, jsonEncode(userData));
  }

  Future<Map<String, dynamic>?> getUserData() async {
    final data = _secureBox.get(AppConstants.userDataKey);
    if (data != null) {
      return jsonDecode(data);
    }
    return null;
  }

  // App Settings
  Future<void> setThemeMode(String themeMode) async {
    await _prefs.setString(AppConstants.themeKey, themeMode);
  }

  Future<String?> getThemeMode() async {
    return _prefs.getString(AppConstants.themeKey);
  }

  Future<void> setLanguage(String language) async {
    await _prefs.setString(AppConstants.languageKey, language);
  }

  Future<String?> getLanguage() async {
    return _prefs.getString(AppConstants.languageKey);
  }

  // Generic Storage Methods
  Future<void> setString(String key, String value) async {
    await _prefs.setString(key, value);
  }

  Future<String?> getString(String key) async {
    return _prefs.getString(key);
  }

  Future<void> setInt(String key, int value) async {
    await _prefs.setInt(key, value);
  }

  Future<int?> getInt(String key) async {
    return _prefs.getInt(key);
  }

  Future<void> setDouble(String key, double value) async {
    await _prefs.setDouble(key, value);
  }

  Future<double?> getDouble(String key) async {
    return _prefs.getDouble(key);
  }

  Future<void> setBool(String key, bool value) async {
    await _prefs.setBool(key, value);
  }

  Future<bool?> getBool(String key) async {
    return _prefs.getBool(key);
  }

  Future<void> setStringList(String key, List<String> value) async {
    await _prefs.setStringList(key, value);
  }

  Future<List<String>?> getStringList(String key) async {
    return _prefs.getStringList(key);
  }

  Future<void> remove(String key) async {
    await _prefs.remove(key);
  }

  Future<void> clear() async {
    await _prefs.clear();
  }

  // Secure Storage Methods
  Future<void> setSecureString(String key, String value) async {
    await _secureBox.put(key, value);
  }

  Future<String?> getSecureString(String key) async {
    return _secureBox.get(key);
  }

  Future<void> setSecureData(String key, Map<String, dynamic> data) async {
    await _secureBox.put(key, jsonEncode(data));
  }

  Future<Map<String, dynamic>?> getSecureData(String key) async {
    final data = _secureBox.get(key);
    if (data != null) {
      return jsonDecode(data);
    }
    return null;
  }

  Future<void> removeSecure(String key) async {
    await _secureBox.delete(key);
  }

  Future<void> clearSecure() async {
    await _secureBox.clear();
  }

  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  // Check if user is first time user
  Future<bool> isFirstTimeUser() async {
    return await getBool('is_first_time_user') ?? true;
  }

  Future<void> setFirstTimeUser(bool isFirstTime) async {
    await setBool('is_first_time_user', isFirstTime);
  }
}
