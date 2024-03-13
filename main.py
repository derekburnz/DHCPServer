"""
Derek Burns, Muhammad Maahir Abdul Aziz
derekburns@cmail.carleton.ca, muhammadmaahirabdul@cmail.carleton.ca
02.1.2024
"""

import time

class IPPool:
  
    def __init__(self):
        self.current_pool = [0, 0, 0, 0]
        self.used_ips = {}
        self.lease_time = 60  # Lease time in seconds

    def get_next_ip(self):
        # Find the lowest available IP address
        for i in range(256 ** 4):
            ip = ".".join(map(str, self.current_pool))
            if ip not in self.used_ips or time.time() > self.used_ips[ip]:
                self.used_ips[ip] = time.time() + self.lease_time
                return ip
            self.increment_ip()

    def increment_ip(self):
        # Increment the IP address in the pool
        for i in range(3, -1, -1):
            if self.current_pool[i] < 255:
                self.current_pool[i] += 1
                break
            else:
                self.current_pool[i] = 0

    def release_ip(self, ip_address):
      # Release the IP address if it exists
      if ip_address in self.used_ips:
          del self.used_ips[ip_address]
          self.current_pool = [0, 0, 0, 0]

    def renew_ip(self, ip_address):
        # Renew the lease time if the IP address exists
        if ip_address in self.used_ips:
            self.used_ips[ip_address] = time.time() + self.lease_time

    def check_status(self, ip_address):
      # Check the status of the IP address
      if ip_address in self.used_ips:
          expiration_time = self.used_ips[ip_address]
          current_time = time.time()
          if current_time < expiration_time:
              time_left = int(expiration_time - current_time)
              return f"{ip_address} ASSIGNED - Time Left: {time_left} seconds"
          else:
              self.release_ip(ip_address)
              return f"{ip_address} AVAILABLE"
      else:
        return f"{ip_address} AVAILABLE"


def handle_ask(ip_pool):
    next_ip = ip_pool.get_next_ip()
    print(f"Offer {next_ip}")

def handle_renew(ip_address, ip_pool):
    # Validate if the provided IP address is in a valid format
    try:
        ip_parts = list(map(int, ip_address.split(".")))
        if len(ip_parts) != 4 or any(part < 0 or part > 255 for part in ip_parts):
            raise ValueError("Invalid IP address format")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Check if the provided IP address is currently in use
    if ip_address in ip_pool.used_ips:
        ip_pool.renew_ip(ip_address)
        print(f"RENEWED for {ip_address}")
    else:
        print(f"Error: {ip_address} is not currently in use")



def handle_release(ip_address, ip_pool):
    # Validate if the provided IP address is in a valid format
    try:
        ip_parts = list(map(int, ip_address.split(".")))
        if len(ip_parts) != 4 or any(part < 0 or part > 255 for part in ip_parts):
            raise ValueError("Invalid IP address format")
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Check if the provided IP address is currently in use
    if ip_address in ip_pool.used_ips:
        ip_pool.release_ip(ip_address)
        print(f"RELEASED for {ip_address}")
    else:
        print(f"Error: {ip_address} is not currently in use")

def handle_status(ip_address, ip_pool):
  # Validate if the provided IP address is in a valid format
  try:
      ip_parts = list(map(int, ip_address.split(".")))
      if len(ip_parts) != 4 or any(part < 0 or part > 255 for part in ip_parts):
          raise ValueError("Invalid IP address format")
  except ValueError as e:
      print(f"Error: {e}")
      return

  status = ip_pool.check_status(ip_address)
  print(status)


def main_menu():
    ip_pool = IPPool()

    while True:
        user_input = input("Enter command (ASK, RENEW #.#.#.#, RELEASE #.#.#.#, STATUS #.#.#.#): ").strip().upper()

        if user_input == "ASK":
            handle_ask(ip_pool)
        elif user_input.startswith("RENEW "):
            ip_address = user_input.split(" ")[1]
            handle_renew(ip_address, ip_pool)
        elif user_input.startswith("RELEASE "):
            ip_address = user_input.split(" ")[1]
            handle_release(ip_address, ip_pool)
        elif user_input.startswith("STATUS "):
            ip_address = user_input.split(" ")[1]
            handle_status(ip_address, ip_pool)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main_menu()
