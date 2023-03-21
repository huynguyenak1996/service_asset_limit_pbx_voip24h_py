import pexpect
import sys

p = pexpect.spawn('asterisk -r')
# Kết nối tới CLI của Asterisk
# cli = pexpect.spawn('asterisk -r')
print(p)
# cli.expect('CLI>')
#
# # Gửi command cdr show status và đợi kết quả
# cli.sendline('cdr show status')
# cli.expect('CDR logging:')
#
# # Lấy dữ liệu kết quả và tách ra các thông tin cần thiết
# output = cli.before.decode('utf-8')
# cdr_status = output.split('\r\n')[1:-1]
# for line in cdr_status:
#     data = line.split()
#     print(f"Total time: {data[0]}, Calls: {data[1]}, CDRs: {data[2]}")